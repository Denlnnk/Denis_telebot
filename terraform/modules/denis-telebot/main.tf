resource "aws_s3_bucket_object" "default_lambda_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = var.lambda_zip_file_name
  acl    = "private"
  source = "../denis-telebot.zip"
}

resource "aws_lambda_function" "denis-telebot" {
  function_name = "denis-telebot"
  role = aws_iam_role.default.arn
  handler = var.lambda_handler_name
  s3_bucket = aws_s3_bucket.lambda_bucket.bucket
  s3_key = var.lambda_zip_file_name
  memory_size = 512
  timeout = 300
  runtime = "python3.9"

  depends_on = [aws_s3_bucket_object.default_lambda_zip]

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

resource "aws_iam_policy" "lambda-basic-execution-policy" {
  name        = "Lambda-basic-execution"
  description = "Allows lambda to create log groups in CloudWatch"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "basic-execution-attachment" {
  role       = aws_iam_role.default.name
  policy_arn = aws_iam_policy.lambda-basic-execution-policy.arn
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

resource "aws_api_gateway_rest_api" "den-telebot-api" {
  name        = "den-telebot-api"
  description = "API exposed to access telegram bot lambda"
}

resource "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.den-telebot-api.id
  parent_id   = aws_api_gateway_rest_api.den-telebot-api.root_resource_id
  path_part   = "lambda"
}

resource "aws_api_gateway_method" "POST" {
  rest_api_id   = aws_api_gateway_rest_api.den-telebot-api.id
  resource_id   = aws_api_gateway_resource.root.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda-integration" {
  rest_api_id             = aws_api_gateway_rest_api.den-telebot-api.id
  resource_id             = aws_api_gateway_resource.root.id
  http_method             = aws_api_gateway_method.POST.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.denis-telebot.invoke_arn

  # Transforms the incoming XML request to JSON
  request_templates = {
    "application/xml" = <<EOF
{
   "body" : $input.json('$')
}
EOF
  }
}

resource "aws_api_gateway_deployment" "den-telebot-api-deployment" {
  rest_api_id = aws_api_gateway_rest_api.den-telebot-api.id
  depends_on = [
    "aws_api_gateway_integration.lambda-integration"
  ]

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.den-telebot-api.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "test-stage" {
  deployment_id = aws_api_gateway_deployment.den-telebot-api-deployment.id
  rest_api_id   = aws_api_gateway_rest_api.den-telebot-api.id
  stage_name    = "test"
}