resource "google_cloud_scheduler_job" "job" {
  name             = "OTGC update"
  description      = "OTGC scheduled task"
  schedule         = "0 */1 * * *"
  time_zone        = "Europe/Paris"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = var.endpoint
    body        = base64encode("{\"username\":\"${var.username}\", \"password\":\"${var.password}\"}")
  }
}