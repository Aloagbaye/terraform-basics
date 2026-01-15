"""
Part D: Connect Pub/Sub → Pipeline (Event-Driven MLOps)

This Cloud Function receives Pub/Sub events and triggers
Vertex AI Pipeline jobs based on the event type.

Example event types:
- new_data_arrived: Trigger data validation pipeline
- retrain_model: Trigger model retraining pipeline
- deploy_model: Trigger model deployment pipeline
"""

import base64
import json
import logging
import os
from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_ml_event(event, context):
    """
    Cloud Function entry point for Pub/Sub ML events.
    
    Expected event format:
    {
        "data": base64_encoded_json,
        "attributes": {
            "event_type": "new_data_arrived" | "retrain_model" | "deploy_model"
        }
    }
    """
    try:
        # Get configuration from environment variables
        project_id = os.environ.get("PROJECT_ID")
        region = os.environ.get("REGION", "us-central1")
        bucket_name = os.environ.get("BUCKET_NAME")
        service_account = os.environ.get("SERVICE_ACCOUNT_EMAIL")
        pipeline_template = os.environ.get("PIPELINE_TEMPLATE", "gs://{bucket}/pipelines/simple_pipeline.json")
        
        if not all([project_id, bucket_name, service_account]):
            logger.error("Missing required environment variables: PROJECT_ID, BUCKET_NAME, SERVICE_ACCOUNT_EMAIL")
            return
        
        # Parse Pub/Sub message
        event_type = None
        message_data = {}
        
        if "attributes" in event:
            event_type = event["attributes"].get("event_type")
        
        if "data" in event:
            payload = base64.b64decode(event["data"]).decode("utf-8")
            message_data = json.loads(payload)
            # If event_type not in attributes, try to get it from message data
            if not event_type:
                event_type = message_data.get("event_type")
        
        if not event_type:
            logger.warning("No event_type found in message. Using default: new_data_arrived")
            event_type = "new_data_arrived"
        
        logger.info(f"Received ML event: {event_type}")
        logger.info(f"Message data: {message_data}")
        
        # Initialize Vertex AI
        aiplatform.init(
            project=project_id,
            location=region,
            staging_bucket=f"gs://{bucket_name}/pipelines"
        )
        
        # Determine which pipeline to run based on event type
        pipeline_path = pipeline_template.format(bucket=bucket_name)
        display_name = f"ml-pipeline-{event_type}-{context.timestamp}"
        
        # Create pipeline job
        job = aiplatform.PipelineJob(
            display_name=display_name,
            template_path=pipeline_path,
            pipeline_root=f"gs://{bucket_name}/pipelines",
            parameter_values={
                "event_type": event_type,
                **message_data  # Pass through any additional parameters
            }
        )
        
        logger.info(f"Submitting pipeline job: {display_name}")
        logger.info(f"Pipeline template: {pipeline_path}")
        logger.info(f"Event type: {event_type}")
        
        # Submit the pipeline job
        job.submit(service_account=service_account)
        
        logger.info(f"✅ Pipeline job submitted successfully!")
        logger.info(f"Job name: {job.resource_name}")
        logger.info(f"Job ID: {job.job_id}")
        
        return {
            "status": "success",
            "event_type": event_type,
            "job_id": job.job_id,
            "job_name": job.resource_name,
            "display_name": display_name
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing ML event: {str(e)}", exc_info=True)
        raise
