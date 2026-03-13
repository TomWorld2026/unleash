resource "aws_apigatewayv2_api" "api" {

  name          = "candidate-api-${var.region}"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "greet" {

  api_id = aws_apigatewayv2_api.api.id

  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.greeter.invoke_arn
}

resource "aws_apigatewayv2_route" "greet" {

  api_id = aws_apigatewayv2_api.api.id

  route_key = "POST /greet"

  target = "integrations/${aws_apigatewayv2_integration.greet.id}"

  authorization_type = "JWT"

  authorizer_id = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_integration" "dispatch" {

  api_id = aws_apigatewayv2_api.api.id

  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.dispatcher.invoke_arn
}

resource "aws_apigatewayv2_route" "dispatch" {

  api_id = aws_apigatewayv2_api.api.id

  route_key = "POST /dispatch"

  target = "integrations/${aws_apigatewayv2_integration.dispatch.id}"

  authorization_type = "JWT"

  authorizer_id = aws_apigatewayv2_authorizer.cognito.id
}

data "aws_caller_identity" "current" {}

resource "aws_kms_key" "log_key" {
  description             = "KMS key for API Gateway logs"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [

      {
        Sid = "EnableRootPermissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = "kms:*"
        Resource = "*"
      },

      {
        Sid = "AllowCloudWatchLogs"
        Effect = "Allow"
        Principal = {
          Service = "logs.${var.region}.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/aws/apigateway/candidate-api-${var.region}"
  retention_in_days = 7

  kms_key_id = aws_kms_key.log_key.arn
}

resource "aws_apigatewayv2_stage" "default" {

  api_id = aws_apigatewayv2_api.api.id
  name   = "$default"

  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn

    format = jsonencode({
      requestId      = "$context.requestId"
      sourceIp       = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      responseLength = "$context.responseLength"
    })
  }  
}

resource "aws_apigatewayv2_authorizer" "cognito" {
  api_id           = aws_apigatewayv2_api.api.id
  authorizer_type  = "JWT"
  name             = "cognito-authorizer"
  identity_sources = ["$request.header.Authorization"]

  jwt_configuration {
    audience = [var.cognito_user_pool_client_id]

    issuer = "https://cognito-idp.us-east-1.amazonaws.com/${var.cognito_user_pool_id}"
  }
}

output "api_url" {
  value = aws_apigatewayv2_api.api.api_endpoint
}