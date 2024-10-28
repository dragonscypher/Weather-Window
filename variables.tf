variable "aws_region" {
  description = "The AWS region where resources will be created."
  default     = "us-east-1"
}

variable "iot_thing_name" {
  description = "Name of the IoT Thing"
  default     = "WeatherMonitoringThing"
}

variable "lambda_function_name_prefix" {
  description = "Prefix for Lambda function names."
  default     = "WeatherLambda"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table for storing sensor data"
  default     = "ESP32_Data"
}
