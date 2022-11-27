# Remove all created resources
terraform destroy

# First, get the name of the bucket
string_file=$(cat main.tf)
regex='bucket  = \"tf_state_otgc_([a-zA-Z0-9]+)\"'
[[ "$string_file" =~ $regex ]]
random_chars="${BASH_REMATCH[1]}"

# Reset main.tf
sed -i -r 's/tf_state_otgc_[a-zA-Z0-9]+/MANUAL_EDIT_WRITE_YOUR_BUCKET/m' ./main.tf

# Set up Google project
project_file=$(cat terraform.tfvars)
regex='project = \"([a-zA-Z0-9_-]+)\"'
[[ "$string_file" =~ $regex ]]
PROJECT_ID="${BASH_REMATCH[1]}"
gcloud config set project $PROJECT_ID

# Remove the state bucket
gsutil rm -r gs://tf_state_otgc_${random_chars}

# Remove config and values files
rm terraform.tfvars
cd ../ && rm config.ini