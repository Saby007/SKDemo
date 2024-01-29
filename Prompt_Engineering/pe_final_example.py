from colorama import Fore, Style, init
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.core_plugins import ConversationSummaryPlugin
import os

async def pe_final_example():
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

    # Import the ConversationSummaryPlugin
    kernel.import_plugin(
        ConversationSummaryPlugin(kernel=kernel), plugin_name="ConversationSummaryPlugin"
    )

    print(Fore.MAGENTA+"Thanks for selecting Prompt Engineering Final Example")
    #print(Fore.MAGENTA+"Lets find the intent of user's request")

    # Import the OrchestratorPlugin from the plugins directory.
    function = kernel.import_semantic_plugin_from_directory("./Prompt_Engineering", "prompts")

    history = []

    while(True):
        print("Type 'q' to return")
        request = input("User > ") #I want to send an email to the marketing team celebrating their recent milestone
        if(request == "q"):
            break
        else:
            variables = kernel.create_new_context()
            variables["request"] = request
            variables["history"] = "\n".join(history)
            
            # Run the prompt
            chat = function["chat"]
            result = await chat.invoke_async(context=variables)
            
            # Add the request to the history
            history.append("User: " + request)
            history.append("Assistant" + result.result)
            print("Assistant > " + result.result)

