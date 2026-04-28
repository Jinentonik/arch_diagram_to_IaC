data "archive_file" "generate_architecture_description" {
  type        = "zip"
  source_dir = "${path.root}/code/generate_architecture_description"
  output_path = "${path.root}/code/zip/generate_architecture_description/generate_architecture_description.zip"
}
data "archive_file" "generate_deployment_sequence" {
  type        = "zip"
  source_dir = "${path.root}/code/generate_deployment_sequence"
  output_path = "${path.root}/code/zip/generate_deployment_sequence/generate_deployment_sequence.zip"
}
data "archive_file" "generate_module_description" {
  type        = "zip"
  source_dir = "${path.root}/code/generate_module_description"
  output_path = "${path.root}/code/zip/generate_module_description/generate_module_description.zip"
}
data "archive_file" "generate_module_prompt" {
  type        = "zip"
  source_dir = "${path.root}/code/generate_module_prompt"
  output_path = "${path.root}/code/zip/generate_module_prompt/generate_module_prompt.zip"
}
data "archive_file" "get_image" {
  type        = "zip"
  source_dir = "${path.root}/code/get_image"
  output_path = "${path.root}/code/zip/get_image/get_image.zip"
}
data "archive_file" "modular_stack_generator_main" {
  type        = "zip"
  source_dir = "${path.root}/code/modular_stack_generator_main"
  output_path = "${path.root}/code/zip/modular_stack_generator_main/modular_stack_generator_main.zip"
}
data "archive_file" "zip_iac_file" {
  type        = "zip"
  source_dir = "${path.root}/code/zip_iac_file"
  output_path = "${path.root}/code/zip/zip_iac_file/zip_iac_file.zip"
}

resource "aws_lambda_function" "generate_architecture_description" {
	function_name = "tf-generate_architecture_description"
	filename      = "${path.root}/code/zip/generate_architecture_description/generate_architecture_description.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 60
	source_code_hash = data.archive_file.generate_architecture_description.output_base64sha256
}

resource "aws_lambda_function" "generate_deployment_sequence" {
	function_name = "tf-generate_deployment_sequence"
	filename      = "${path.root}/code/zip/generate_deployment_sequence/generate_deployment_sequence.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 60
	source_code_hash = data.archive_file.generate_deployment_sequence.output_base64sha256
}

resource "aws_lambda_function" "generate_module_description" {
	function_name = "tf-generate_module_description"
	filename      = "${path.root}/code/zip/generate_module_description/generate_module_description.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 60
	source_code_hash = data.archive_file.generate_module_description.output_base64sha256
}

resource "aws_lambda_function" "generate_module_prompt" {
	function_name = "tf-generate_module_prompt"
	filename      = "${path.root}/code/zip/generate_module_prompt/generate_module_prompt.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 60
	source_code_hash = data.archive_file.generate_module_prompt.output_base64sha256
}

resource "aws_lambda_function" "get_image" {
	function_name = "tf-get_image"
	filename      = "${path.root}/code/zip/get_image/get_image.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 60
	source_code_hash = data.archive_file.get_image.output_base64sha256
}

resource "aws_lambda_function" "modular_stack_generator_main" {
	function_name = "tf-modular_stack_generator_main"
	filename      = "${path.root}/code/zip/modular_stack_generator_main/modular_stack_generator_main.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 300
	source_code_hash = data.archive_file.modular_stack_generator_main.output_base64sha256
}

resource "aws_lambda_function" "zip_iac_file" {
	function_name = "tf-zip_iac_file"
	filename      = "${path.root}/code/zip/zip_iac_file/zip_iac_file.zip"
	handler       = "lambda_function.lambda_handler"
	runtime       = "python3.14"
	role          = aws_iam_role.iamr_lambda.arn
	timeout       = 60
	source_code_hash = data.archive_file.zip_iac_file.output_base64sha256
}