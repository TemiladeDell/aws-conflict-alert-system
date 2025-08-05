resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "log_bucket" {
  bucket = "conflict-zone-alert-logs-${random_id.suffix.hex}"
  force_destroy = true
}

resource "random_id" "bucket_id" {
  byte_length = 4
}

resource "aws_s3_bucket" "conflict_data_storage" {
  bucket = "conflict-zone-alert-data-${random_id.bucket_id.hex}"
  force_destroy = true

  tags = {
    Name        = "ConflictZoneDataBucket"
    Environment = "Dev"
  }
}

