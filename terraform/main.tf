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
  function_name        = "otgc-public_http"
  function_entry_point = "helloWorld"
  # function_url         = "otgc-${var.project}-${locals.timestamp}"
}
