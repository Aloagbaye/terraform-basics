output "bucket_name" {
  value = google_storage_bucket.example_bucket.name
}

output "environment" {
  value = var.environment
}

output "service_account_email" {
  value = google_service_account.ml_service_account.email
}

output "pubsub_topic" {
  value = google_pubsub_topic.ml_topic.name
}

output "pubsub_subscription" {
  value = google_pubsub_subscription.ml_subscription.name
}

output "pipeline_root" {
  value = "gs://${google_storage_bucket.example_bucket.name}/pipelines"
}
