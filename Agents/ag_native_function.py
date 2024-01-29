from colorama import Fore, Style, init
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os

async def ag_native_function():
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

    
    print(Fore.MAGENTA+"Thanks for selecting Agents Native Function")
    #print(Fore.MAGENTA+"Lets find the intent of user's request")

    # Import the OrchestratorPlugin from the plugins directory.
    #function = kernel.import_semantic_plugin_from_directory("./Agents", "plugins")
    function = kernel.import_native_plugin_from_directory("./Agents/plugins", "native")

    while(True):
        print("Type 'q' to return")
        request = input("User > ") #I want to send an email to the marketing team celebrating their recent milestone
        if(request == "q"):
            break
        else:
            # Run the prompt
            native = function["GenerateNumberThreeOrHigher"]
            result = await native.invoke_async(input=request)
            
            print("Assistant > " + result.result)

