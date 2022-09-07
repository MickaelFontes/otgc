# Deploy with Terraform

To easily deploy the GCP resources we need to use OTGC, we will use Terraform.

You'll first need to:

1. To make things easy, open a [Cloud Shell](https://console.cloud.google.com/home/dashboard?cloudshell=true) inside your project
2. Clone this GitHub repo inside your Cloud Shell VM.
3. Create a bucket storage to store your Terraform state remotely. Copy its name.
4. Activate the Cloud Function API
5. At the root of the `terraform` folder, under the `backend "gcs"` section, replace `MANUAL_EDIT_WRITE_YOUR_BUCKET` with the name of the bucket you just created.
6. Copy `terraform.tfvars.example`, rename it `terraform.tfvars` and fill it with your values (`username` and `password` to authentificate on OnBoard).
7. Copy `config_example.ini`, rename it `config.ini` and fill the fields `REFRESH_TOKEN`, `CLIENT_ID` and `CLIENT_SECRET` with your values.
8. Ensure a few  minutes have elapsed since you activated the Cloud Function API and then deploy using `terrafom init` and `terraform apply`
9. ANJOY
