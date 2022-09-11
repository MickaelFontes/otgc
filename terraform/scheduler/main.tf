resource "google_cloud_scheduler_job" "job" {
  name             = "otgc_update"
  description      = "OTGC scheduled task"
  schedule         = var.schedule
  time_zone        = "Europe/Paris"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = var.endpoint
    headers     =  {
      Content-Type = "application/json"
    }
    body        = base64encode("{\"username\":\"${var.username}\", \"password\":\"${var.password}\"}")
  }
}