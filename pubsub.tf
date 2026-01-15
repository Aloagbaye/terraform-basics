resource "google_pubsub_topic" "ml_topic" {
  name = "${var.pubsub_topic_name}-${var.environment}"

  labels = {
    environment = var.environment
    managed_by  = "terraform"
    purpose     = "ml-events"
  }
}

resource "google_pubsub_subscription" "ml_subscription" {
  name  = "${var.pubsub_subscription_name}-${var.environment}"
  topic = google_pubsub_topic.ml_topic.name

  ack_deadline_seconds = 20

  message_retention_duration = "604800s" # 7 days

  labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}

