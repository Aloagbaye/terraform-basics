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
    google_project_service.cloudbuild
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
  }

  event_trigger {
    trigger_region = var.region
    pubsub_topic   = google_pubsub_topic.ml_topic.id
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
  }
}
