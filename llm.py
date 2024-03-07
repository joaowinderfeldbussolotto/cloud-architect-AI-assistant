import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get('CLAUDE_API_KEY'),
)

def get_diagram_response(encoded_image, type):
    prompt = f'''
    You are an expert AWS Certified Solutions Architect. Your role is to help customers understand AWS Architeture diagrams and provide Infra-as-code as a snippet. 
    Given the image provided, you will explain the architeture and provide CloudFormation code to create that infrastructure that will help customers solve their problem effectively.
    Describe the services being used and the possible reason for usage. Pay attention to the regions and avaliabilty zones!
    You can provide serverless.yml or CloudFormation.yaml code as IaC, choose wisely.
    Finish your prompt telling that if there any questions, the user is free to ask
    '''
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": type,
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print(message)

    return message.content[0].text


