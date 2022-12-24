variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "AWS region"
}

variable "aws_access_key" {
  default = ""
}
variable "aws_secret_key" {
  default = ""
}