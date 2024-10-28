terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "aws-iot-weather-monitoring/terraform.tfstate"
    region = "us-east-1"
  }
}
