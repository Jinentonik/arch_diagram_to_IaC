resource "aws_dynamodb_table" "jobs" {
  name         = "tf-diagram-to-terraform-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "jobId"

  attribute {
    name = "jobId"
    type = "S"
  }
}
