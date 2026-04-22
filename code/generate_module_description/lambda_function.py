import json
import boto3

def generate_module_descriptions(architecture_description_dict , modules_description_prompt):
    bedrock_runtime = boto3.client('bedrock-runtime')
    architecture_description =architecture_description_dict['architecture_description']
    
    prompt = modules_description_prompt + architecture_description
    print("MODULE DESCRIPTION PROMPT", prompt )
    
    
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 5048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    
                ],
            }
        ],
    }

    # modelId = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
    modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
    accept = 'application/json'
    contentType = 'application/json'

    # Invoke the model and get the response
    response = bedrock_runtime.invoke_model(modelId=modelId, body=json.dumps(request_body))
    response_body = json.loads(response['body'].read())

    # Extract generated text
    if isinstance(response_body['content'], list) and len(response_body['content']) > 0:
        module_descriptions = response_body['content'][0].get('text', '')
        module_descriptions.strip("```json\n").strip("```")
        print(type(module_descriptions))
        print("Module Descriptions",module_descriptions)
        
        return module_descriptions
    else:
        return {"module_descriptions": "Unexpected response format"}

def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        print(f"File content: {content}")
        return content
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Check your deployment package.")

def lambda_handler(event, context):
    # TODO implement
    file_path = "./module_description_prompt.txt"
    modules_description_prompt = read_file(file_path)
    arch_description_dict = event.get('arch_description_dict')
    module_descriptions = generate_module_descriptions(arch_description_dict , modules_description_prompt)

    return {
        'statusCode': 200,
        'module_descriptions': module_descriptions
    }
