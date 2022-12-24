variable "lambda_handler_name" {
  type = string
  default = "lambda_function.py"
}

variable "lambda_zip_file_name" {
  type = string
  default = "denis-telebot.zip"
}

variable "region" {}
variable "service_name" {}