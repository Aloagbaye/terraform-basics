resource "google_project_service" "vertex_ai" {
  service = "aiplatform.googleapis.com"
}
