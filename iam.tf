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
