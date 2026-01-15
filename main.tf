resource "google_storage_bucket" "example_bucket" {
  name          = "${var.project_id}-terraform-demo-bucket"
  location      = var.region
  force_destroy = var.environment == "dev"

  uniform_bucket_level_access = true

  labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}

resource "google_storage_bucket_iam_member" "bucket_access" {
  bucket = google_storage_bucket.example_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.ml_service_account.email}"
}
