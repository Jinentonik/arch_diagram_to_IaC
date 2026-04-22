import json
import boto3

def generate_deployment_sequence(modules_description , deployment_sequence_prompt):

    #modules_description =modules_description_dict['modules_description']
    bedrock_runtime = boto3.client('bedrock-runtime')
    prompt = deployment_sequence_prompt + modules_description
    
    deployment_sequence_dict ={ 'modules_description' : ''}
    
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10000,
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

    modelId = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
    accept = 'application/json'
    contentType = 'application/json'

    # Invoke the model and get the response
    response = bedrock_runtime.invoke_model(modelId=modelId, body=json.dumps(request_body))
    response_body = json.loads(response['body'].read())

    # Extract generated text
    if isinstance(response_body['content'], list) and len(response_body['content']) > 0:
        module_descriptions_with_sequence = response_body['content'][0].get('text', '')
        deployment_sequence_dict['modules_description']=module_descriptions_with_sequence
        print("DEPLOYMENT SEQUENCE", deployment_sequence_dict)
        
        
        
        return deployment_sequence_dict

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
    file_path = "./deployment_sequence_prompt.txt"
    deployment_sequence_prompt = read_file(file_path)
    module_descriptions = event.get('module_descriptions', '')
    module_descriptions = generate_deployment_sequence(module_descriptions, deployment_sequence_prompt)
    print("type", type(module_descriptions))
    return {
        'statusCode': 200,
        'module_descriptions': module_descriptions
    }
