
resource "aws_lambda_function" "denis-telebot" {
  function_name = "denis-telebot"
  role = aws_iam_role.default.arn
  handler = var.lambda_handler_name
  s3_bucket = aws_s3_bucket.lambda_bucket.bucket
  s3_key = var.lambda_zip_file_name
  memory_size = 512
  timeout = 300
  runtime = "python3.9"

  environment {
    variables = {
      TOKEN = "5599768818:AAG1TpKn0ai06O6md4A8dCHdivAM4dfdwXg"
      API_LAYER_TOKEN = "JougRDP5JFwn5Z1PQECca4khbWKCQf2Z"
      INSTA_USERNAME = "danciel22"
      INSTA_PASSWORD = "newpasswordforme"
    }
  }
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "denis-telebot-lambda-bucket"
}

resource "aws_iam_role" "default" {
  name_prefix = "denis-telebot-role"
  assume_role_policy = data.aws_iam_policy_document.allow_assume_role_denis_telebot_lambda.json
}

data "aws_iam_policy_document" "allow_assume_role_denis_telebot_lambda" {
  statement {
    effect = "Allow"
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}