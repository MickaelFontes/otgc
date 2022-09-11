# gcloud services enable cloudfunctions.googleapis.com
random_chars=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)
random_int=$(( RANDOM % 60 ))

if [ $# -ne 7 ]; then
    echo "You did not provide the rigth number of arguments !!"
    exit 1
fi

# Print parameters and let user check them
echo "Check if these values seem corect to you"
echo "PROJECT_ID: $1"
echo "CLIENT_ID: $2"
echo "CLIENT_SECRET: $3"
echo "REFRESH_TOKEN: $4"
echo "CALENDAR_ID: $5"
echo "ONBAORD_USERNAME: $6"
echo "ONBOARD_PASSWORD: $7"

echo "If everything is correct, enter 'yes'
Only 'yes' will be accepted to approve."

read -p 'Enter a value: ' entervalue

if [[ $entervalue -ne 'yes' ]]; then
    echo "Incorrect value. Install canceled."
    exit 1
fi

# Create and update the Terraform main.tf with your state bucket name
gsutil mb gs://tf_state_otgc_${random_chars}
gcloud services enable cloudfunctions.googleapis.com
sleep 30
sed -i "s/\(MANUAL_EDIT_WRITE_YOUR_BUCKET\)/tf_state_otgc_${random_chars}/m" ./main.tf

# Create terraform.tfvars.example
cp terraform.tfvars.example terraform.tfvars

sed -i "s/\(your_project\)/$1/m" ./terraform.tfvars
sed -i "s/\(your_onboard_username\)/$6/m" ./terraform.tfvars
sed -i "s/\(your_onboard_password\)/$7/m" ./terraform.tfvars
sed -i "s/\(your_function\)/otgc_function_${random_chars}/m" ./terraform.tfvars
sed -i "s/\(your_cron_expression\)/${random_int} \*\/1 \* \* \*\\ /m" ./terraform.tfvars

# Update values in config.ini
cd ../

cp config_example.ini config.ini
sed -i "s/\yourcalendar@group.calendar.google.com\)/$5/m" ./config.ini
sed -i "s/\(your_client_id\)/$2/m" ./config.ini
sed -i "s/\(your_client_secret\)/$3/m" ./config.ini
sed -i "s/\(your_refresh_token\)/$4/m" ./config.ini

cd terraform

# Apply the Terraform config
terraform init && terraform apply