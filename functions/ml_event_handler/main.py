import base64
import json
import logging

def handle_ml_event(event, context):
    if "data" in event:
        payload = base64.b64decode(event["data"]).decode("utf-8")
        message = json.loads(payload)
        logging.info(f"Received ML event: {message}")
    else:
        logging.warning("No data found in event")
