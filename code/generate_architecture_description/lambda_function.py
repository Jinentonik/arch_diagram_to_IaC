import json
import boto3
import os

def generate_architecture_description(prompt, encoded_image):
    
    """
    Generates an architecture description using Amazon Bedrock's Claude 4.5 Sonnet model by analyzing 
    provided text prompt and image input.

    This function sends a request to the Claude 3.5 Sonnet model through Amazon Bedrock Runtime, 
    combining both text and image inputs to generate a descriptive analysis of architectural elements.

    Args:
        prompt (str): The text prompt guiding the model's analysis of the architecture.
        encoded_image (str): A base64-encoded PNG image string of the architecture to be analyzed.

    Returns:
        dict: A dictionary containing the generated architecture description with the following structure:
            {
                "architecture_description": str
            }
            If successful, contains the generated description text.
            If unsuccessful, contains the message "Unexpected response format".

    Raises:
        May raise exceptions from bedrock_runtime.invoke_model() related to:
        - Invalid model invocation
        - API throttling
        - Authentication/authorization issues
        - Invalid input format

    Example:
        >>> prompt = "Describe the architectural style and key features of this building"
        >>> encoded_image = "base64_encoded_image_string"
        >>> result = generate_architecture_description(prompt, encoded_image)
        >>> print(result["architecture_description"])

    Notes:
        - The function uses the Claude 4.5 Sonnet model (version 20240620-v1:0)
        - Maximum token limit is set to 2048 tokens
        - Expects PNG image format
        - Prints the generated description to stdout in addition to returning it
    """
    bedrock_runtime = boto3.client('bedrock-runtime')
    # Prepare the request body
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": encoded_image,
                        },
                    },
                ],
            }
        ],
    }

    # modelId = 'anthropic.claude-sonnet-4-5-20250929-v1:0'
    modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'

    # Invoke the model and get the response
    response = bedrock_runtime.invoke_model(modelId=modelId, body=json.dumps(request_body))
    response_body = json.loads(response['body'].read())

    # Extract generated text
    if isinstance(response_body['content'], list) and len(response_body['content']) > 0:
        generated_text = response_body['content'][0].get('text', '')
        print("Architecture Description",generated_text)
        
        return {"architecture_description": generated_text}
    else:
        return {"architecture_description": "Unexpected response format"}

def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        print(f"File content: {content}")
        return content
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Check your deployment package.")

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
    
    file_path = "./arch_prompt.txt"
    arch_prompt = read_file(file_path)

    print(event)
    encoded_image = event.get('encoded_image', '')
    job_id = event.get("jobId")
    
    arch_description_dict=generate_architecture_description(arch_prompt, encoded_image)
    print(arch_description_dict)

    update_job(
        job_id=job_id,
        status="ANALYZING_ARCHITECTURE",
        progress=30
    )
    return {
        'statusCode': 200,
        'arch_description_dict': arch_description_dict,
        'jobId': job_id
    }
