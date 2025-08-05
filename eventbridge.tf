resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "daily-conflict-check"
  description         = "Triggers the Lambda every day to check for conflicts"
  schedule_expression = "rate(1 day)" # Or cron expression
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "lambda"
  arn       = aws_lambda_function.conflict_alert_function.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.conflict_alert_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_trigger.arn
}
