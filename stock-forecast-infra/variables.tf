variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "db_username" {
  description = "RDS PostgreSQL master username"
  type        = string
}

variable "db_password" {
  description = "RDS PostgreSQL master password"
  type        = string
}
`