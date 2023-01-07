echo "Going to upload zip file to lambda"

if [ -d "package" ]; then
  rmdir package
fi

mkdir package
pip install --target ./package -r requirements.txt
# shellcheck disable=SC2164
cd package
zip -r ../denis-telebot.zip .
# shellcheck disable=SC2103
cd ..
zip -r denis-telebot.zip bot

# shellcheck disable=SC2164
cd ./terraform
terraform plan
terraform apply


