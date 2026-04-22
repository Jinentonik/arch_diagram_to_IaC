import json
import boto3
from datetime import datetime
import re
from pprint import pprint
import uuid

def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        print(f"File content: {content}")
        return content
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Check your deployment package.")

def write_code_to_s3(
    code_str,
    bucket_name,
    stack_dirname,
    module_name,
    log_stream,
    s3_prefix=""
):
   
    extension = ".tf"

    filename = (
        module_name.lower()
        .replace(' module', '')
        .replace(' ', '_')
        + "_stack"
        + extension
    )

    # Build S3 key
    now = datetime.now()
    now_str = now.strftime('%Y_%m_%d_%H_%M')
    key_parts = [s3_prefix.strip('/'), stack_dirname, now_str, log_stream, filename]
    # s3_key = f"{s3_prefix.strip('/')}/{stack_dirname}/{now_str}/{filename}"
    s3_key = "/".join(part for part in key_parts if part)

    # Upload to S3
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=code_str.encode("utf-8"),
        ContentType="text/plain"
    )

    s3_uri = f"s3://{bucket_name}/{s3_key}"
    print("CODE UPLOADED TO", s3_uri)

    return s3_uri

def write_log_to_s3(
    prompt_response: str,
    step: str,
    bucket_name: str,
    s3_prefix: str
) -> str:
    """
    Writes prompt responses as a human-readable text file to Amazon S3.
    """

    s3_client = boto3.client("s3", region_name="us-east-1")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"log_{step}_{timestamp}.txt"

    s3_key = f"{s3_prefix.rstrip('/')}/{step}/{filename}"

    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=prompt_response,          # ✅ PASS STRING DIRECTLY
        ContentType="text/plain; charset=utf-8"
    )

    return f"s3://{bucket_name}/{s3_key}"


def generate_step2_prompt(step_1_response):
    
    """
    Generate prompt for a subsequent step in the reasoning path based on  the response of a previous step
    """
    file_path = "./module_prompt_step2.txt"
    step_2_prompt = read_file(file_path)
    step_1_response_dict={'initial_terraform_stack' : step_1_response}
    initial_terraform_stack_string=step_1_response_dict['initial_terraform_stack']
    step_2_prompt=step_2_prompt + '\n' + initial_terraform_stack_string
    print("TYPE" , type(step_2_prompt))
    
    return step_2_prompt,initial_terraform_stack_string

def generate_step3_prompt(step_2_response, initial_terraform_stack_string):
    """
    Generates a prompt for step 3 by combining the previous step's response with Terraform stack information.

    Args:
        step_2_response (str): The response from step 2 containing IAM roles information
        code_language (str): The target programming language for code generation
        initial_terraform_stack_string (str): The initial Terraform stack configuration string

    Returns:
        str: A formatted prompt string containing the combined information from all inputs,
             including the Terraform stack details and IAM roles/policies
    """

    pprint(initial_terraform_stack_string)
    file_path = "./module_prompt_step3.txt"
    step_3_prompt = read_file(file_path)
    
    print("STEP 3 PROMPT STR" , step_3_prompt)
    step_2_response_dict= {'roles_list' : step_2_response}
    roles_list= step_2_response_dict['roles_list']
    step_3_prompt=step_3_prompt + '\n'  +  initial_terraform_stack_string +'\n' + "##IAM Roles and policies to be included##" + '\n' + roles_list
    print("FINAL")
    print(step_3_prompt)
    return step_3_prompt

def generate_step4_prompt(step_3_response):

    """

    Generate prompt for a subsequent step in the reasoning path based on  the response of a previous step

    """
    file_path = "./module_prompt_step4.txt"
    step_4_prompt = read_file(file_path)
    step_3_response_dict={'terraform_stack_with_roles' : step_3_response}
    terraform_stack_with_roles=step_3_response_dict['terraform_stack_with_roles']
    step_4_prompt=step_4_prompt + '\n'  + terraform_stack_with_roles
    pprint(step_4_prompt)
    return step_4_prompt

def get_ai_response(prompt: str):
    """
    Calls Amazon Bedrock Claude 3.5 Sonnet model (anthropic.claude-sonnet-4-6) synchronously.
    Ignores session, api_key, and base_url for compatibility with previous signature.
    """
    bedrock_runtime = boto3.client('bedrock-runtime')
    # modelId = 'anthropic.claude-sonnet-4-6'
    modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 20000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"}
                ],
            }
        ],
    }
    response = bedrock_runtime.invoke_model(modelId=modelId, body=json.dumps(request_body))
    response_body = json.loads(response['body'].read())
    if isinstance(response_body['content'], list) and len(response_body['content']) > 0:
        generated_text = response_body['content'][0].get('text', '')
        return generated_text
    else:
        return "Unexpected response format"

def code_generation_do_it_all(module_name, module_prompt, log_stream):
    """
    """
    print("STARTING STACK GENERATION FOR MODULE NAME:" , module_name)
    print(f"Task {module_name} started at {datetime.now()}")
    module_prompt_suffix_file_path = "./module_prompt_suffix.txt"
    deployment_sequence_prompt = read_file(module_prompt_suffix_file_path)
    step_1_prompt= module_prompt + '\n' + deployment_sequence_prompt
    
    # Step 1: Perplexity step 1
    
    print("-----------------STEP 1 PROMPT---------------")
    pprint( step_1_prompt)
    
    step_1_response= get_ai_response(step_1_prompt)
    
    write_log_to_s3(step_1_response, "step1", "test-a2a-bucket", "generated_code_log")
    print("-----------------STEP 1 RESPONSE---------------")
    pprint( step_1_response)
    
    # Step 2: Perplexity Step 2
    pprint("-----------------STEP 2 PROMPT---------------")
    step_2_prompt,initial_terraform_stack_string= generate_step2_prompt(step_1_response)
    pprint(step_2_prompt)
    
    print("-----------------STEP 2 RESPONSE---------------")
    step_2_response= get_ai_response(step_2_prompt)
    
    write_log_to_s3(step_2_response, "step2", "test-a2a-bucket", "generated_code_log")
    pprint(step_2_response)
    
    # Step 3: Perplexity Step 3
    print("-----------------STEP 3 PROMPT---------------")
    step_3_prompt = generate_step3_prompt(step_2_response,initial_terraform_stack_string)
    print("step 3 prompt", step_3_prompt)
    
    print("-----------------STEP 3 RESPONSE---------------")
    step_3_response= get_ai_response(step_3_prompt)
    
    write_log_to_s3(step_3_response, "step3", "test-a2a-bucket", "generated_code_log")
    pprint( step_3_response)
    
    # Step 4: Perplexity Step 4
    step_4_prompt = generate_step4_prompt(step_3_response)
    print("step 4 prompt" , step_4_prompt)
    
    step_4_response= get_ai_response(step_4_prompt)
    write_log_to_s3(step_4_response, "step4", "test-a2a-bucket", "generated_code_log")
    pprint(step_4_response)
    
    # Step 5: Write final code to s3
    codefilepath = write_code_to_s3(step_4_response, "test-a2a-bucket","generated_code", module_name, log_stream)
    
    print(f"Task {module_name} ended at {datetime.now()}")

    return  codefilepath

def modular_stack_generator_main(module_prompt_dict, log_stream):
    responses = []

    for module_name, module_prompt in module_prompt_dict.items():
        result = code_generation_do_it_all(module_name, module_prompt, log_stream)
        responses.append(result)

    return responses

def lambda_handler(event, context):
    # TODO implement
    module_prompt_dict = event.get('module_prompt_dict')
    module_list = event.get('module_list')
    log_stream = context.log_stream_name
    result = modular_stack_generator_main(module_prompt_dict, log_stream)
    # module_list = event.get('module_list', '')  
    
    
    return {
        'statusCode': 200,
        'body': "Success",
        'source_s3_uris': result
    }
