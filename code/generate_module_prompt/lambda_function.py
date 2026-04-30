import json
import boto3
import os

def generate_module_prompts(deployment_sequence_dict):
    
    # Parse dictionary
    
    modules_description =deployment_sequence_dict['modules_description']
    print("Modules Description", modules_description)
    modules_description_dict=json.loads(modules_description)
    
    # Create empty dictionary to store prompts
    module_prompt_dict = {}   
    
    keys = list(modules_description_dict.keys())
    print(keys)
    
    stack_names = list(modules_description_dict.values())[-1] 
    print("stack_names" , stack_names)
    
    # Skip first and last keys, process only module information
    for key in keys[1:-1]:
        module_name = key
        print("Module Name", module_name) 
        module_description = modules_description_dict[key]
        print("Module Description" , module_description)
        
        # Construct prompt for each module
        # prompt = (
        #     f"Generate a AWS CDK stack in {language_name} for module name '{module_name}' "
        #     f"with the following module description: {module_description}. "
        #     "Ensure Implementation reflects all interaction mentioned. Use the Basename of the Module as the name of the CDK stack, without the substring 'Module' included in the name of the stack"
        # )
        prompt = (
            f"Generate a Terraform module using HashiCorp Configuration Language (HCL) for the module named '{module_name}'. "
            f"Use the following module description: {module_description}. "
            "Ensure the implementation fully reflects all interactions mentioned in the description. "
            "Use the basename of the module as the Terraform module name, excluding the substring 'Module'. "
            "Include well-structured Terraform files (e.g., main.tf, variables.tf, outputs.tf) with appropriate "
            "AWS providers, resources, variables, and outputs following Terraform best practices."
        )
        
        # Add to prompt dictionary with module name as key
        module_prompt_dict[module_name] = prompt
    return module_prompt_dict,stack_names

def update_job(job_id, status, progress, download_url=None, error_message=None):
    lambda_client = boto3.client("lambda")
    update_job_lambda_arn = os.getenv('UPDATE_JOB_LAMBDA_ARN')
    payload = {
        "jobId": job_id,
        "status": status,
        "progress": progress
    }

    if download_url:
        payload["downloadUrl"] = download_url

    if error_message:
        payload["errorMessage"] = error_message

    lambda_client.invoke(
        FunctionName=update_job_lambda_arn,
        InvocationType="Event",
        Payload=json.dumps(payload).encode("utf-8")
    )

def lambda_handler(event, context):
    # TODO implement
    print(event)
    job_id = event.get('jobId')
    module_descriptions = event.get('module_descriptions', '')

    module_prompt_dict,modules_list = generate_module_prompts(module_descriptions)
    
    update_job(
        job_id=job_id,
        status="PREPARING_IAC",
        progress=65
    )

    return {
        'statusCode': 200,
        'module_prompt_dict': module_prompt_dict,
        'modules_list': modules_list,
        'jobId': job_id
    }
