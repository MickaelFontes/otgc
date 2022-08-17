terraform {
  required_providers {
	google = {
	  source = "hashicorp/google"
	  version = "4.32.0 "
	}
  }
  backend "gcs" {
   bucket  = var.state_bucket
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
  function_entry_point = "main"
}
