
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
