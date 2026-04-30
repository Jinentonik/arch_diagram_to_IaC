resource "aws_cloudwatch_event_rule" "s3_object_created" {
  name = "tf-diagram-uploaded-rule"

  event_pattern = jsonencode({
    source      = ["aws.s3"],
    detail-type = ["Object Created"],
    detail = {
      bucket = {
        name = [aws_s3_bucket.input.id]
      }
      object = {
        key = [{
          prefix = "uploads/"
        }]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "start_step_function" {
  rule      = aws_cloudwatch_event_rule.s3_object_created.name
  target_id = "tf-InvokeStepFunctionToConvertDiagramToTerraformCode"
  arn       = module.step_function.state_machine_arn
  role_arn  = aws_iam_role.eventbridge_stepfunction.arn

  input_transformer {
    input_paths = {
      bucket = "$.detail.bucket.name"
      key    = "$.detail.object.key"
    }

    input_template = <<EOF
{
  "bucket": <bucket>,
  "objectKey": <key>
}
EOF
  }
}