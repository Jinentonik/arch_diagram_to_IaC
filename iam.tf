
resource "aws_iam_role" "iamr_lambda" {
  name = "iamr-tf-lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "iamr_lambda_bedrock" {
  role       = aws_iam_role.iamr_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_iam_role_policy_attachment" "iamr_lambda_s3" {
  role       = aws_iam_role.iamr_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "iamr_lambda_basic" {
  role       = aws_iam_role.iamr_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role" "iamr_step_function" {
  name = "iamr-tf-step-function"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "states.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "iamr_step_function_lambda" {
  role       = aws_iam_role.iamr_step_function.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
}

resource "aws_iam_role_policy_attachment" "iamr_step_function_cwlogs" {
  role       = aws_iam_role.iamr_step_function.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_role_policy" "lambda_xtra_access" {
  name = "lambda-extra-permission"
  role = aws_iam_role.iamr_lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem"
        ]
        Resource = aws_dynamodb_table.jobs.arn
      },
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = aws_lambda_function.update_job_status.arn
      }
    ]
  })
  depends_on = [aws_dynamodb_table.jobs, aws_lambda_function.update_job_status]
}


resource "aws_iam_role" "eventbridge_stepfunction" {
  name = "tf-eventbridge-start-stepfunction"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "events.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "eventbridge_stepfunction" {
  role = aws_iam_role.eventbridge_stepfunction.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "states:StartExecution"
      Resource = module.step_function.state_machine_arn
    }]
  })
}