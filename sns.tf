resource "aws_sns_topic_subscription" "email_sub" {
  topic_arn = "arn:aws:sns:us-east-1:274603885640:conflict-alert-topic"
  protocol  = "email"
  endpoint  = "temiladedell@gmail.com"
}
