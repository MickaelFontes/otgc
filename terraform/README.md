# Deploy with Terraform

To easily deploy the GCP resources we need to use OTGC, we will use Terraform.

You'll first need to:

1. To make things easy, open a [Cloud Shell](https://console.cloud.google.com/home/dashboard?cloudshell=true) inside your project
2. Enable Cloud Function API
3. Create a bucket storage to store your Terraform state remotely
4. Check the root `main.tf` and choose to use Cloud Scheduler or not
   (if you use Cloud Scheduler, uncomment the `my_scheduler` module and write your credentials in the corresponding fields)
5. Create the corresponding `terraform.tfvars` file with your values
6. Ensure a few  minutes have elapsed since you activated the Cloud Function API and then deploy using `terrafom init` and `terraform apply`
7. ANJOY
