"""
Upload compiled pipeline JSON to GCS bucket.

This script uploads the compiled pipeline JSON file to the GCS bucket
so it can be referenced by the Cloud Function and pipeline jobs.

Usage:
    python scripts/upload_pipeline.py --bucket BUCKET_NAME --pipeline pipelines/simple_pipeline/simple_pipeline.json
"""

import argparse
from google.cloud import storage


def upload_pipeline(bucket_name: str, pipeline_json_path: str, destination_path: str = None):
    """
    Upload pipeline JSON file to GCS bucket.
    
    Args:
        bucket_name: GCS bucket name
        pipeline_json_path: Local path to pipeline JSON file
        destination_path: Destination path in bucket (default: pipelines/simple_pipeline.json)
    """
    if not destination_path:
        # Extract filename from path
        import os
        filename = os.path.basename(pipeline_json_path)
        destination_path = f"pipelines/{filename}"
    
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_path)
    
    # Upload file
    print(f"Uploading {pipeline_json_path} to gs://{bucket_name}/{destination_path}")
    blob.upload_from_filename(pipeline_json_path)
    
    print(f"✅ Pipeline uploaded successfully!")
    print(f"GCS path: gs://{bucket_name}/{destination_path}")
    
    return f"gs://{bucket_name}/{destination_path}"


def main():
    parser = argparse.ArgumentParser(
        description="Upload compiled pipeline JSON to GCS"
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="GCS bucket name"
    )
    parser.add_argument(
        "--pipeline",
        default="pipelines/simple_pipeline/simple_pipeline.json",
        help="Path to compiled pipeline JSON file"
    )
    parser.add_argument(
        "--destination",
        help="Destination path in bucket (default: pipelines/{filename})"
    )
    
    args = parser.parse_args()
    
    try:
        gcs_path = upload_pipeline(
            bucket_name=args.bucket,
            pipeline_json_path=args.pipeline,
            destination_path=args.destination
        )
        print(f"\nUse this path in your pipeline jobs: {gcs_path}")
        return 0
    except Exception as e:
        print(f"❌ Error uploading pipeline: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
