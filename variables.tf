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
