resource "google_project_service" "functions" {
  service = "cloudfunctions.googleapis.com"
}

resource "google_project_service" "run" {
  service = "run.googleapis.com"
}

resource "google_project_service" "eventarc" {
  service = "eventarc.googleapis.com"
}

resource "google_project_service" "cloudbuild" {
  service = "cloudbuild.googleapis.com"
}

resource "google_cloudfunctions2_function" "ml_event_handler" {
  depends_on = [
    google_project_service.functions,
    google_project_service.run,
    google_project_service.eventarc,
    google_project_service.cloudbuild,
    google_storage_bucket_iam_member.cloudbuild_bucket_access,
    google_project_iam_member.cloudbuild_run_admin,
    google_project_iam_member.cloudbuild_functions_developer,
    google_project_iam_member.cloudbuild_artifact_registry_writer,
    google_project_iam_member.cloudbuild_logging_writer,
    google_service_account_iam_member.cloudbuild_service_account_user
  ]
  name     = "ml-event-handler-${var.environment}"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "handle_ml_event"
    source {
      storage_source {
        bucket = google_storage_bucket.example_bucket.name
        object = "ml-event-handler.zip"
      }
    }
  }

  service_config {
    service_account_email = google_service_account.ml_service_account.email
    available_memory      = "256Mi"
    timeout_seconds       = 60
    
    environment_variables = {
      PROJECT_ID            = var.project_id
      REGION                = var.region
      BUCKET_NAME           = google_storage_bucket.example_bucket.name
      SERVICE_ACCOUNT_EMAIL = google_service_account.ml_service_account.email
      PIPELINE_TEMPLATE     = "gs://${google_storage_bucket.example_bucket.name}/pipelines/simple_pipeline.json"
      ENVIRONMENT           = var.environment
    }
  }

  event_trigger {
    trigger_region = var.region
    pubsub_topic   = google_pubsub_topic.ml_topic.id
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
  }
}
