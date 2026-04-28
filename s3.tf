resource "aws_s3_bucket" "input" {
  bucket = "diagram-to-terraform-input"
}

resource "aws_s3_bucket" "output" {
  bucket = "diagram-to-terraform-output"
}
