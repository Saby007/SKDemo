from colorama import Fore, Style, init
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os

async def ag_semantic_function():
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

    
    print(Fore.MAGENTA+"Thanks for selecting Agents Semantic Function")
    #print(Fore.MAGENTA+"Lets find the intent of user's request")

    # Import the OrchestratorPlugin from the plugins directory.
    function = kernel.import_semantic_plugin_from_directory("./Agents", "plugins")

    history = []

    while(True):
        print("Type 'q' to return")
        request = input("User > ") #I want to send an email to the marketing team celebrating their recent milestone
        if(request == "q"):
            break
        else:
            variables = kernel.create_new_context()
            variables["request"] = request
                        
            # Run the prompt
            semantic = function["semantic"]
            result = await semantic.invoke_async(context=variables)
            
            print("Assistant > " + result.result)

