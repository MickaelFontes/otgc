terraform {
  required_providers {
	google = {
	  source = "hashicorp/google"
	  version = "4.32.0 "
	}
  }
  backend "gcs" {
   bucket  = "MANUAL_EDIT_WRITE_YOUR_BUCKET"
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
  function_name        = var.function_name
  function_entry_point = "helloWorld"
}

# Comment if you want to config the cloud scheduler using credentials in clear text
# /!\ Your credentials will be saved in Cloud Scheduler, in the IaC and in the Terraform state
module "my_scheduler" {
  source = "./scheduler"
  username = var.username
  password = var.password
  endpoint = module.my_function.function_url
  schedule = var.schedule
}