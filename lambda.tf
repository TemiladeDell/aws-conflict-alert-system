resource "aws_lambda_function" "conflict_alert_function" {
  function_name = "conflictZoneAlert"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.12"
  filename      = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  timeout = 40

  tags = {
    Name        = "ConflictZoneAlertLambda"
    Environment = "Dev"
  }
}
