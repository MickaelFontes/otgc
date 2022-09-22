variable "project" {  
  type = string
  description = "Project ID of your GCP project. It is the ID. Be careful"
}
variable "region" {
  type = string
  description = "GCP region used"
  default = "europe-west1"
}
variable "username" {
  type = string
  description = "OnBoard username"
}
variable "password" {  
  type = string
  description = "OnBoard password"
}
variable "schedule" {
  type = string
  description = "Cron expression used by the Cloud Scheduler"
  default = "0 */1 * * *"
}
variable "function_name" {
  type = string
  description = "Name of the Cloud Funnction to deploy - used in the url to access"
}