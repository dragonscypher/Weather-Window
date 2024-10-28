provider "aws" {
  region = "us-east-1"
}

resource "aws_iot_thing" "weather_monitoring_thing" {
  name = "WeatherMonitoringThing"
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_custom_policy" {
  name   = "lambda_custom_policy"
  role   = aws_iam_role.lambda_execution_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action: [
          "dynamodb:PutItem",
          "ssm:GetParameter",
          "apigatewaymanagementapi:PostToConnection",
          "ssm:PutParameter"
        ],
        Resource: "*",
        Effect: "Allow"
      }
    ]
  })
}

resource "aws_lambda_function" "send_message_lambda" {
  filename         = "SendMessage-AWS-Lambda-function.zip"
  function_name    = "SendMessageLambdaFunction"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "SendMessage-AWS-Lambda-function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("SendMessage-AWS-Lambda-function.zip")
}

resource "aws_lambda_function" "storage_lambda" {
  filename         = "Storage-AWS-lambda-function.zip"
  function_name    = "StorageLambdaFunction"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "Storage-AWS-lambda-function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("Storage-AWS-lambda-function.zip")
}

resource "aws_lambda_function" "connect_lambda" {
  filename         = "connect-AWS-Lambda-function.zip"
  function_name    = "ConnectLambdaFunction"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "connect-AWS-Lambda-function.handler"
  runtime          = "nodejs14.x"
  source_code_hash = filebase64sha256("connect-AWS-Lambda-function.zip")
}

resource "aws_iot_endpoint" "weather_monitoring_endpoint" {
  endpoint_type = "iot:Data-ATS"
}

resource "aws_api_gateway_v2_api" "websocket_api" {
  name          = "WeatherMonitoringWebSocketAPI"
  protocol_type = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

resource "aws_dynamodb_table" "esp32_data" {
  name           = "ESP32_Data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "date"

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "temperature"
    type = "N"
  }

  attribute {
    name = "humidity"
    type = "N"
  }
}

output "iot_endpoint" {
  value = aws_iot_endpoint.weather_monitoring_endpoint.endpoint_address
}

output "iot_thing_name" {
  value = aws_iot_thing.weather_monitoring_thing.name
}
