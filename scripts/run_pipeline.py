"""
Part C: Upload & Run Pipeline (Programmatic)

This script demonstrates how to programmatically submit and run
Vertex AI Pipelines from Python code.

Usage:
    python scripts/run_pipeline.py --pipeline simple_pipeline.json --event-type new_data_arrived
"""

import argparse
import os
from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs


def run_pipeline(
    project_id: str,
    region: str,
    bucket_name: str,
    pipeline_json_path: str,
    service_account_email: str,
    event_type: str = "manual_run",
    display_name: str = None
):
    """
    Initialize Vertex AI and submit a pipeline job.
    
    Args:
        project_id: GCP project ID
        region: GCP region
        bucket_name: GCS bucket name for staging
        pipeline_json_path: Path to compiled pipeline JSON file
        service_account_email: Service account to run the pipeline
        event_type: Type of event triggering the pipeline
        display_name: Optional display name for the pipeline run
    """
    # Initialize Vertex AI
    aiplatform.init(
        project=project_id,
        location=region,
        staging_bucket=f"gs://{bucket_name}/pipelines"
    )
    
    # Set display name
    if not display_name:
        display_name = f"simple-ml-pipeline-{event_type}"
    
    # Create and submit pipeline job
    job = aiplatform.PipelineJob(
        display_name=display_name,
        template_path=pipeline_json_path,
        pipeline_root=f"gs://{bucket_name}/pipelines",
        parameter_values={
            "event_type": event_type
        } if event_type else {}
    )
    
    print(f"Submitting pipeline job: {display_name}")
    print(f"Pipeline template: {pipeline_json_path}")
    print(f"Pipeline root: gs://{bucket_name}/pipelines")
    print(f"Service account: {service_account_email}")
    
    # Run the pipeline
    job.run(service_account=service_account_email)
    
    print(f"\n✅ Pipeline job submitted successfully!")
    print(f"Job name: {job.resource_name}")
    print(f"View in console: https://console.cloud.google.com/vertex-ai/pipelines/runs/{job.resource_name}?project={project_id}")
    
    return job


def main():
    parser = argparse.ArgumentParser(
        description="Run a Vertex AI Pipeline programmatically"
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="GCP Project ID"
    )
    parser.add_argument(
        "--region",
        default="us-central1",
        help="GCP region (default: us-central1)"
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="GCS bucket name for pipeline staging"
    )
    parser.add_argument(
        "--pipeline",
        default="pipelines/simple_pipeline/simple_pipeline.json",
        help="Path to compiled pipeline JSON file"
    )
    parser.add_argument(
        "--service-account",
        required=True,
        help="Service account email to run the pipeline"
    )
    parser.add_argument(
        "--event-type",
        default="manual_run",
        help="Event type triggering the pipeline (default: manual_run)"
    )
    parser.add_argument(
        "--display-name",
        help="Optional display name for the pipeline run"
    )
    
    args = parser.parse_args()
    
    # Verify pipeline file exists
    if not os.path.exists(args.pipeline):
        print(f"❌ Error: Pipeline file not found: {args.pipeline}")
        return 1
    
    try:
        job = run_pipeline(
            project_id=args.project_id,
            region=args.region,
            bucket_name=args.bucket,
            pipeline_json_path=args.pipeline,
            service_account_email=args.service_account,
            event_type=args.event_type,
            display_name=args.display_name
        )
        return 0
    except Exception as e:
        print(f"❌ Error running pipeline: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
