module "step_function" {
  source = "terraform-aws-modules/step-functions/aws"
  name   = "tf-generate-IaC"
  # create_role = false
  use_existing_role = true
  role_arn          = aws_iam_role.iamr_step_function.arn
  definition = templatefile("${path.root}/step_function_definition/generate-IaC.json", {
    GET_IMAGE_LAMBDA_ARN                         = aws_lambda_function.get_image.arn,
    GENERATE_ARCHITECTURE_DESCRIPTION_LAMBDA_ARN = aws_lambda_function.generate_architecture_description.arn,
    GENERATE_MODULE_DESCRIPTION_LAMBDA_ARN       = aws_lambda_function.generate_module_description.arn,
    GENERATE_DEPLOYMENT_SEQUENCE_LAMBDA_ARN      = aws_lambda_function.generate_deployment_sequence.arn,
    GENERATE_MODULE_PROMPT_LAMBDA_ARN            = aws_lambda_function.generate_module_prompt.arn,
    MODULAR_STACK_GENERATOR_MAIN_LAMBDA_ARN      = aws_lambda_function.modular_stack_generator_main.arn,
    ZIP_IAC_FILE_LAMBDA_ARN                      = aws_lambda_function.zip_iac_file.arn
  })
  # service_integrations = {
  #     lambda = [
  #         aws_lambda_function.generate_architecture_description.arn,
  #         aws_lambda_function.generate_deployment_sequence.arn,
  #         aws_lambda_function.generate_module_description.arn,
  #         aws_lambda_function.generate_module_prompt.arn,
  #         aws_lambda_function.get_image.arn,
  #         aws_lambda_function.modular_stack_generator_main.arn,
  #         aws_lambda_function.zip_iac_file.arn
  #     ]
  # }

}