from colorama import Fore, Style, init
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
import os


class WebSearchEnginePlugin:
    """
    A search engine plugin.
    """

    from semantic_kernel.orchestration.kernel_context import KernelContext
    from semantic_kernel.plugin_definition import (
        kernel_function,
        kernel_function_context_parameter,
    )

    def __init__(self, connector) -> None:
        self._connector = connector

    @kernel_function(description="Performs a web search for a given query", name="searchAsync")
    @kernel_function_context_parameter(
        name="query",
        description="The search query",
    )
    async def search(self, query: str, context: KernelContext) -> str:
        query = context.variables.get("query")
        result = await self._connector.search(query, num_results=5, offset=0)
        #print("Query:", query)
        #print(result)
        return str(result)

async def ag_planner():
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

    
    print(Fore.MAGENTA+"Thanks for selecting Agents Planner Demo")
    #print(Fore.MAGENTA+"Lets find the intent of user's request")

    # Basic Planner
    print(Fore.MAGENTA+"----------------Basic Planner Demo----------------")
    # The BasicPlanner produces a JSON-based plan that aims to solve the provided ask sequentially and evaluated in order.
    from semantic_kernel.planning.basic_planner import BasicPlanner
    from semantic_kernel.core_plugins.text_plugin import TextPlugin
    from semantic_kernel.core_plugins.conversation_summary_plugin import ConversationSummaryPlugin
    
    text_plugin = kernel.import_plugin(TextPlugin(), "TextPlugin")
    summary_plugin = kernel.import_plugin(ConversationSummaryPlugin(kernel), "ConversationSummaryPlugin")

    planner = BasicPlanner()

    #sk_prompt = """{{$input}}
    #            Rewrite the above in the style of Shakespeare.
    #            """
    #shakespeareFunction = kernel.create_semantic_function(prompt_template=sk_prompt,function_name="shakespeare", plugin_name="ShakespearePlugin", max_tokens=2000, temperature=0.8,)
    ask = """ Summarize the content in less than 100 words and convert the text to uppercase . Content is "This is a basic planner demo for everyone!!" """

    basic_plan = await planner.create_plan(ask, kernel)
    print("Plan generated.....")
    print(Fore.LIGHTGREEN_EX)
    print(basic_plan.generated_plan)
    
    results = await planner.execute_plan(basic_plan, kernel)
    print(results)


    # Sequentical Planner
    print(Fore.MAGENTA+"----------------Sequentical Planner Demo----------------")
    # The sequential planner is an XML-based step-by-step planner
    from semantic_kernel.planning.sequential_planner import SequentialPlanner

    planner = SequentialPlanner(kernel)

    print(Fore.LIGHTGREEN_EX)
    sequential_plan = await planner.create_plan(goal=ask)

    for step in sequential_plan._steps:
        print(step.description)

    
    result = await sequential_plan.invoke_async()
    print(result)

    # Action Planner

    print(Fore.MAGENTA+"----------------Action Planner Demo----------------")
    # The action planner takes in a list of functions and the goal, and outputs a single function to use that is appropriate to meet that goal.

    from semantic_kernel.planning import ActionPlanner

    planner = ActionPlanner(kernel)

    from semantic_kernel.core_plugins import (
    FileIOPlugin,
    MathPlugin,
    TextPlugin,
    TimePlugin,
    )

    kernel.import_plugin(MathPlugin(), "math")
    kernel.import_plugin(FileIOPlugin(), "fileIO")
    kernel.import_plugin(TimePlugin(), "time")
    kernel.import_plugin(TextPlugin(), "text")
    
    ask = "What is the sum of 110 and 990?"

    plan = await planner.create_plan(goal=ask)

    result = await plan.invoke_async()

    print(Fore.LIGHTGREEN_EX)

    print(result)
    
    
    # Stepwise Planner

    print(Fore.MAGENTA+"----------------Stepwise Planner Demo----------------")

    # Stepwise Planner is based off the paper from MRKL (Modular Reasoning, Knowledge and Language) and is similar to other papers like 
    # ReACT (Reasoning and Acting in Language Models). At the core, the stepwise planner allows for the AI to form "thoughts" and "observations" 
    # and execute actions based off those to achieve a user's goal. This continues until all required functions are complete and a final output is generated.


    from semantic_kernel.connectors.search_engine import BingConnector

    BING_API_KEY = os.environ.get('BING_API_KEY')
    connector = BingConnector(BING_API_KEY)
    kernel.import_plugin(WebSearchEnginePlugin(connector), plugin_name="WebSearch")


    from semantic_kernel.planning import StepwisePlanner
    from semantic_kernel.planning.stepwise_planner.stepwise_planner_config import (
        StepwisePlannerConfig
    )

    planner = StepwisePlanner(kernel, StepwisePlannerConfig(max_iterations=10, min_iteration_time_ms=1000))

    ask = """Who won the first IPL in the year 2008?"""

    plan = planner.create_plan(goal=ask)
    

    result = await plan.invoke_async()
    print(Fore.LIGHTGREEN_EX)

    print(result)

    print(Fore.MAGENTA+"----------------End of Planner Demo----------------")
    
    


