# Get project number for Cloud Build service account
data "google_project" "project" {
  project_id = var.project_id
}

resource "google_service_account" "ml_service_account" {
  account_id   = var.service_account_name
  display_name = "${var.environment} ML Service Account"
}

resource "google_project_iam_member" "gcs_access" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.ml_service_account.email}"
}

resource "google_project_iam_member" "vertex_ai_access" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ml_service_account.email}"
}

resource "google_pubsub_topic_iam_member" "publisher_access" {
  topic  = google_pubsub_topic.ml_topic.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.ml_service_account.email}"
}

resource "google_pubsub_subscription_iam_member" "subscriber_access" {
  subscription = google_pubsub_subscription.ml_subscription.name
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${google_service_account.ml_service_account.email}"
}

resource "google_project_iam_member" "eventarc_receiver" {
  project = var.project_id
  role    = "roles/eventarc.eventReceiver"
  member  = "serviceAccount:${google_service_account.ml_service_account.email}"
}

# Cloud Build service account permissions
# Cloud Build needs multiple permissions to build and deploy Cloud Functions
resource "google_storage_bucket_iam_member" "cloudbuild_bucket_access" {
  bucket = google_storage_bucket.example_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

data "google_project" "this" {}

locals {
  compute_sa = "${data.google_project.this.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "compute_cloudbuild_builder" {
  project = var.project_id
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${local.compute_sa}"
}

resource "google_project_iam_member" "cloudbuild_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_functions_developer" {
  project = var.project_id
  role    = "roles/cloudfunctions.developer"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_artifact_registry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_logging_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

# Cloud Build needs to act as the runtime service account
resource "google_service_account_iam_member" "cloudbuild_service_account_user" {
  service_account_id = google_service_account.ml_service_account.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "compute_artifactregistry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${local.compute_sa}"
}

resource "google_storage_bucket_iam_member" "compute_source_bucket_reader" {
  bucket = google_storage_bucket.example_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${local.compute_sa}"
}

resource "google_project_iam_member" "vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ml_service_account.email}"
}

