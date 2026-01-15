variable "project_id" {
  description = "GCP Project ID (must be an existing project in your GCP account)"
  type        = string
  
  validation {
    condition     = length(var.project_id) > 0
    error_message = "Project ID cannot be empty. Use 'gcloud projects list' to find your project IDs."
  }
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "service_account_name" {
  description = "Service account name"
  type        = string
}

variable "pubsub_topic_name" {
  description = "Base name for Pub/Sub topic"
  type        = string
}

variable "pubsub_subscription_name" {
  description = "Base name for Pub/Sub subscription"
  type        = string
}
