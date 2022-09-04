locals {
  timestamp = formatdate("YYYY-MM-DD-hh-mm-ss", timestamp())
}
terraform {
  required_providers {
	google = {
	  source = "hashicorp/google"
	  version = "4.32.0 "
	}
  }
  backend "gcs" {
   bucket  = "edt-onboard-tfstate"
   prefix  = "terraform/state"
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

module "my_function" {
  source               = "./function"
  project              = var.project
  function_name        = "otgc-public-http"
  function_entry_point = "helloWorld"
}

# # Uncomment if you want to config the cloud scheduler using credentials in clear text
# # /!\ Your credentials will be saved in Cloud Scheduler, in the IaC and in the Terraform state
# module "my_scheduler" {
#   source = "./scheduler"
#   username = "xxx"
#   password = "xxx"
#   endpoint = module.my_function.function_url
# }