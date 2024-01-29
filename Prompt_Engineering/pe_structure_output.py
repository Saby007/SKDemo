from colorama import Fore, Style, init
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os

async def pe_structure_output():
    # Initialize the kernel
    kernel = sk.Kernel()
    # Add a text or chat completion service using either:
    # kernel.add_text_completion_service()
    # kernel.add_chat_service()
    kernel.add_chat_service("text_completion", AzureChatCompletion(
        deployment_name=os.environ.get("MODEL_NAME"),
        endpoint=os.environ.get("MODEL_ENDPOINT"),
        api_key=os.environ.get("MODEL_API_KEY"),
    ))

    print(Fore.MAGENTA+"Thamks for selecting Prompt Engineering Add Structure to the Output")
    print(Fore.MAGENTA+"Lets find the intent of user's request")

    request = input("Your request: ") #I want to send an email to the marketing team celebrating their recent milestone

    prompt = f"""Instructions: What is the intent of this request?
    Choices: SendEmail, SendMessage, CompleteTask, CreateDocument.
    User Input: {request}
    Intent: """

    semantic_function = kernel.create_semantic_function(prompt)
    print(await semantic_function.invoke_async())

