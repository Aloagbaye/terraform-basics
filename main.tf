resource "google_storage_bucket" "example_bucket" {
  name          = "${var.project_id}-terraform-demo-bucket"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}
