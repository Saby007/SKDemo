from semantic_kernel.core_plugins.time_plugin import TimePlugin
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os
from colorama import Fore, Style, init

# List of out of box plugins:
# https://learn.microsoft.com/en-us/semantic-kernel/agents/plugins/out-of-the-box-plugins?tabs=python


async def ag_out_of_box():
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

    print(Fore.MAGENTA+"Thamks for selecting Agents Out of Box")
    
    kernel.import_plugin(
        TimePlugin(kernel=kernel), plugin_name="time"
    )

    ThePromptTemplate = """
                            Today is: {{time.Date}}
                            Current time is: {{time.Time}}
                            Answer to the following questions using JSON syntax, including the data used.
                            Is it morning, afternoon, evening, or night (morning/afternoon/evening/night)?
                            Is it weekend time (weekend/not weekend)?
                        """

    myKindOfDay = kernel.create_semantic_function(ThePromptTemplate, max_tokens=150)
    myOutput = await myKindOfDay.invoke_async()
    print(myOutput)
    
    




