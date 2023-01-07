variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "AWS region"
}

// put ypu access key here
variable "aws_access_key" {
  default = ""
}

// put your secret key here
variable "aws_secret_key" {
  default = ""
}