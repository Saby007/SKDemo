from colorama import Fore, Style, init
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os

async def pe_provide_context():
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

    print(Fore.MAGENTA+"Thamks for selecting Prompt Engineering Provide Context")
    print(Fore.MAGENTA+"Lets find the intent of user's request")

    request = input("Your request: ") #I agree, can you help me with the full status update to the marketing team that way?

    history = (
    "User input: I hate sending emails, no one ever reads them.\n"
    "AI response: I'm sorry to hear that. Messages may be a better way to communicate."
    )
    prompt = f"""Instructions: What is the intent of this request?\n"
        If you don't know the intent, don't guess; instead respond with "Unknown".
        Choices: SendEmail, SendMessage, CompleteTask, CreateDocument, Unknown.
        User Input: Can you send a very quick approval to the marketing team?
        Intent: SendMessage
        User Input: Can you send the full update to the marketing team?
        Intent: SendEmail
        {history}
        User Input: {request}
        Intent: """

    semantic_function = kernel.create_semantic_function(prompt)
    print(await semantic_function.invoke_async())

