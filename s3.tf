resource "aws_s3_bucket" "input" {
  bucket = "diagram-to-terraform-input"
}

resource "aws_s3_bucket_notification" "input_bucket_notification" {
  bucket      = aws_s3_bucket.input.id
  eventbridge = true
}

resource "aws_s3_bucket_cors_configuration" "input_bucket_cors" {
  bucket = aws_s3_bucket.input.id

  cors_rule {
    #############################################
    # ✅ ADD YOUR CLOUDFRONT DOMAIN HERE
    #############################################
    allowed_origins = [
      "https://${aws_cloudfront_distribution.frontend.domain_name}"
      # Example later:
      # "https://d2omvvlajdbd8u.cloudfront.net"
    ]

    #############################################
    # ✅ Allowed methods for presigned upload
    #############################################
    allowed_methods = [
      "PUT"
    ]

    #############################################
    # ✅ Headers required for presigned URLs
    #############################################
    allowed_headers = ["*"]

    #############################################
    # ✅ Expose headers (optional but safe)
    #############################################
    expose_headers = [
      "ETag"
    ]

    #############################################
    # ✅ Browser caches preflight (seconds)
    #############################################
    max_age_seconds = 300
  }
}


resource "aws_s3_bucket" "output" {
  bucket = "diagram-to-terraform-output"
}

resource "aws_s3_bucket" "frontend" {
  bucket = "diagram-to-terraform-frontend"
}

resource "aws_s3_bucket_ownership_controls" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket                  = aws_s3_bucket.frontend.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "frontend" {
  statement {
    sid = "AllowCloudFrontAccess"

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    actions = ["s3:GetObject"]

    resources = [
      "${aws_s3_bucket.frontend.arn}/*"
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.frontend.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  policy = data.aws_iam_policy_document.frontend.json
}
