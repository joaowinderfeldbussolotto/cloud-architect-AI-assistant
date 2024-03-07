import chainlit as cl
from llm import get_diagram_response
from PIL import Image
import base64

@cl.on_chat_start
async def start():
    files = None

    welcome_msg = f"""
    Welcome to our AWS Diagram Interpreter Bot! 🤖
    Ready to make sense of your AWS architecture diagrams and generate IaC code? 
    Just upload your diagram, and I'll provide a clear explanation along with the corresponding CloudFormation code. 
    Let's simplify your AWS journey together! Feel free to ask any questions along the way. 😊
    """

    while files == None:
        files = await cl.AskFileMessage(
            content=welcome_msg, accept=["image/jpeg", "image/png"]
        ).send()

    file = files[0]

    with open(file.path, "rb") as image_file:
        image_bytes = image_file.read()

    image = cl.Image(path=file.path, name=file.name, display="inline")
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    
    completion = get_diagram_response(encoded_image, file.type)
    await cl.Message(
        content=completion,
        elements=[image]
    ).send()

@cl.on_message
async def main(message: cl.Message):

    await cl.Message(
        content=f"Received: {message.content}",
    ).send()