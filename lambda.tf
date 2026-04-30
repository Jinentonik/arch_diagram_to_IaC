data "archive_file" "upload_diagram" {
  type        = "zip"
  source_dir  = "${path.root}/code/upload_diagram"
  output_path = "${path.root}/code/zip/upload_diagram/upload_diagram.zip"
}
data "archive_file" "job_status" {
  type        = "zip"
  source_dir  = "${path.root}/code/job_status"
  output_path = "${path.root}/code/zip/job_status/job_status.zip"
}
data "archive_file" "update_job_status" {
  type        = "zip"
  source_dir  = "${path.root}/code/update_job_status"
  output_path = "${path.root}/code/zip/update_job_status/update_job_status.zip"
}
data "archive_file" "generate_architecture_description" {
  type        = "zip"
  source_dir  = "${path.root}/code/generate_architecture_description"
  output_path = "${path.root}/code/zip/generate_architecture_description/generate_architecture_description.zip"
}
data "archive_file" "generate_deployment_sequence" {
  type        = "zip"
  source_dir  = "${path.root}/code/generate_deployment_sequence"
  output_path = "${path.root}/code/zip/generate_deployment_sequence/generate_deployment_sequence.zip"
}
data "archive_file" "generate_module_description" {
  type        = "zip"
  source_dir  = "${path.root}/code/generate_module_description"
  output_path = "${path.root}/code/zip/generate_module_description/generate_module_description.zip"
}
data "archive_file" "generate_module_prompt" {
  type        = "zip"
  source_dir  = "${path.root}/code/generate_module_prompt"
  output_path = "${path.root}/code/zip/generate_module_prompt/generate_module_prompt.zip"
}
data "archive_file" "get_image" {
  type        = "zip"
  source_dir  = "${path.root}/code/get_image"
  output_path = "${path.root}/code/zip/get_image/get_image.zip"
}
data "archive_file" "modular_stack_generator_main" {
  type        = "zip"
  source_dir  = "${path.root}/code/modular_stack_generator_main"
  output_path = "${path.root}/code/zip/modular_stack_generator_main/modular_stack_generator_main.zip"
}
data "archive_file" "zip_iac_file" {
  type        = "zip"
  source_dir  = "${path.root}/code/zip_iac_file"
  output_path = "${path.root}/code/zip/zip_iac_file/zip_iac_file.zip"
}

resource "aws_lambda_function" "upload_diagram" {
  function_name    = "tf-upload_diagram"
  filename         = "${path.root}/code/zip/upload_diagram/upload_diagram.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.upload_diagram.output_base64sha256
}

resource "aws_lambda_function" "job_status" {
  function_name    = "tf-job_status"
  filename         = "${path.root}/code/zip/job_status/job_status.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.job_status.output_base64sha256
  environment {
    variables = {
      DDB_TABLE_NAME = aws_dynamodb_table.jobs.id
    }
  }
}

resource "aws_lambda_function" "update_job_status" {
  function_name    = "tf-update_job_status"
  filename         = "${path.root}/code/zip/update_job_status/update_job_status.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.update_job_status.output_base64sha256
  environment {
    variables = {
      DDB_TABLE_NAME = aws_dynamodb_table.jobs.id
    }
  }
}

resource "aws_lambda_function" "generate_architecture_description" {
  function_name    = "tf-generate_architecture_description"
  filename         = "${path.root}/code/zip/generate_architecture_description/generate_architecture_description.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.generate_architecture_description.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
    }
  }
}

resource "aws_lambda_function" "generate_deployment_sequence" {
  function_name    = "tf-generate_deployment_sequence"
  filename         = "${path.root}/code/zip/generate_deployment_sequence/generate_deployment_sequence.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.generate_deployment_sequence.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
    }
  }
}

resource "aws_lambda_function" "generate_module_description" {
  function_name    = "tf-generate_module_description"
  filename         = "${path.root}/code/zip/generate_module_description/generate_module_description.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.generate_module_description.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
    }
  }
}

resource "aws_lambda_function" "generate_module_prompt" {
  function_name    = "tf-generate_module_prompt"
  filename         = "${path.root}/code/zip/generate_module_prompt/generate_module_prompt.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.generate_module_prompt.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
    }
  }
}

resource "aws_lambda_function" "get_image" {
  function_name    = "tf-get_image"
  filename         = "${path.root}/code/zip/get_image/get_image.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.get_image.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
    }
  }
}

resource "aws_lambda_function" "modular_stack_generator_main" {
  function_name    = "tf-modular_stack_generator_main"
  filename         = "${path.root}/code/zip/modular_stack_generator_main/modular_stack_generator_main.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 300
  source_code_hash = data.archive_file.modular_stack_generator_main.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
      S3_CODE_BUCKET = aws_s3_bucket.output.arn
    }
  }
}

resource "aws_lambda_function" "zip_iac_file" {
  function_name    = "tf-zip_iac_file"
  filename         = "${path.root}/code/zip/zip_iac_file/zip_iac_file.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.14"
  role             = aws_iam_role.iamr_lambda.arn
  timeout          = 60
  source_code_hash = data.archive_file.zip_iac_file.output_base64sha256
  environment {
    variables = {
      UPDATE_JOB_LAMBDA_ARN = aws_lambda_function.update_job_status.arn
      S3_CODE_BUCKET = aws_s3_bucket.output.arn
    }
  }
}