import json

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

def lambda_handler(event, context):
    # TODO implement
    module_descriptions = event.get('module_descriptions', '')
    module_prompt_dict,modules_list = generate_module_prompts(module_descriptions)
    print(modules_list)
    print(json.dumps(module_prompt_dict))
    return {
        'statusCode': 200,
        'module_prompt_dict': module_prompt_dict,
        'modules_list': modules_list
    }
