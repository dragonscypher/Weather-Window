output "iot_endpoint" {
  description = "AWS IoT Endpoint for the created thing."
  value       = aws_iot_endpoint.weather_monitoring_endpoint.endpoint_address
}

output "iot_thing_name" {
  description = "The name of the IoT Thing created."
  value       = aws_iot_thing.weather_monitoring_thing.name
}

output "lambda_function_arns" {
  description = "The ARNs of the Lambda functions created."
  value       = [
    aws_lambda_function.send_message_lambda.arn,
    aws_lambda_function.storage_lambda.arn,
    aws_lambda_function.connect_lambda.arn
  ]
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table created."
  value       = aws_dynamodb_table.esp32_data.name
}
