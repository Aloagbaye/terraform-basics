"""
Test script to send Pub/Sub events to trigger ML pipelines.

Usage:
    python scripts/test_pubsub_event.py --event-type new_data_arrived
"""

import argparse
import json
from google.cloud import pubsub_v1


def send_ml_event(
    project_id: str,
    topic_name: str,
    event_type: str,
    message_data: dict = None
):
    """
    Send a Pub/Sub event to trigger ML pipeline.
    
    Args:
        project_id: GCP project ID
        topic_name: Pub/Sub topic name
        event_type: Type of event (new_data_arrived, retrain_model, etc.)
        message_data: Additional message data
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    
    # Prepare message
    if message_data is None:
        message_data = {}
    
    message_data["event_type"] = event_type
    message_json = json.dumps(message_data)
    
    # Publish message
    future = publisher.publish(
        topic_path,
        message_json.encode("utf-8"),
        event_type=event_type
    )
    
    message_id = future.result()
    print(f"✅ Message published successfully!")
    print(f"Message ID: {message_id}")
    print(f"Topic: {topic_path}")
    print(f"Event type: {event_type}")
    print(f"Message data: {message_json}")
    
    return message_id


def main():
    parser = argparse.ArgumentParser(
        description="Send Pub/Sub event to trigger ML pipeline"
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="GCP Project ID"
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Pub/Sub topic name (e.g., ml-events-dev)"
    )
    parser.add_argument(
        "--event-type",
        required=True,
        choices=["new_data_arrived", "retrain_model", "deploy_model", "manual_run"],
        help="Event type to trigger"
    )
    parser.add_argument(
        "--data",
        help="Additional JSON data to include in message"
    )
    
    args = parser.parse_args()
    
    # Parse additional data if provided
    message_data = {}
    if args.data:
        try:
            message_data = json.loads(args.data)
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in --data: {args.data}")
            return 1
    
    try:
        send_ml_event(
            project_id=args.project_id,
            topic_name=args.topic,
            event_type=args.event_type,
            message_data=message_data
        )
        return 0
    except Exception as e:
        print(f"❌ Error sending event: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
