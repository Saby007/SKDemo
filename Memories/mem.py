from typing import Tuple
import semantic_kernel as sk
import os
from colorama import Fore, Style, init
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextEmbedding,
)

import logging
logging.getLogger('aiohttp').setLevel(logging.ERROR)


async def populate_memory(kernel: sk.Kernel, collection) -> None:
    # Add some documents to the semantic memory
    await kernel.memory.save_information(collection=collection, id="info1", text="My name is Andrea")
    await kernel.memory.save_information(collection=collection, id="info2", text="I currently work as a tour guide")
    await kernel.memory.save_information(collection=collection, id="info3", text="I've been living in Seattle since 2005")
    await kernel.memory.save_information(collection=collection, id="info4", text="I visited France and Italy five times since 2015")
    await kernel.memory.save_information(collection=collection, id="info5", text="My family is from New York")

async def search_memory_examples(kernel: sk.Kernel,collection) -> None:
    questions = [
        "what's my name",
        "where do I live?",
        "where's my family from?",
        "where have I traveled?",
        "what do I do for work",
    ]

    for question in questions:
        print(f"Question: {question}")
        result = await kernel.memory.search(collection, question)
        print(f"Answer: {result[0].text}\n")


async def setup_chat_with_memory(kernel: sk.Kernel) -> Tuple[sk.KernelFunctionBase, sk.KernelContext]:
    sk_prompt = """
    ChatBot can have a conversation with you about any topic.
    It can give explicit instructions or say 'I don't know' if
    it does not have an answer.

    Information about me, from previous conversations:
    - {{$fact1}} {{recall $fact1}}
    - {{$fact2}} {{recall $fact2}}
    - {{$fact3}} {{recall $fact3}}
    - {{$fact4}} {{recall $fact4}}
    - {{$fact5}} {{recall $fact5}}

    Chat:
    {{$chat_history}}
    User: {{$user_input}}
    ChatBot: """.strip()

    chat_func = kernel.create_semantic_function(sk_prompt, max_tokens=200, temperature=0.8)

    context = kernel.create_new_context()
    context["fact1"] = "what is my name?"
    context["fact2"] = "where do I live?"
    context["fact3"] = "where's my family from?"
    context["fact4"] = "where have I traveled?"
    context["fact5"] = "what do I do for work?"

    context[sk.core_plugins.TextMemoryPlugin.COLLECTION_PARAM] = "aboutMe"
    context[sk.core_plugins.TextMemoryPlugin.RELEVANCE_PARAM] = "0.8"

    context["chat_history"] = ""

    return chat_func, context

async def chat(kernel: sk.Kernel, chat_func: sk.KernelFunctionBase, context: sk.KernelContext) -> bool:
    try:
        user_input = input("User:> ")
        context["user_input"] = user_input
        #print(f"User:> {user_input}")
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False

    if user_input == "exit":
        print("\n\nExiting chat...")
        return False

    answer = await kernel.run(chat_func, input_vars=context.variables)
    context["chat_history"] += f"\nUser:> {user_input}\nChatBot:> {answer}\n"

    print(f"ChatBot:> {answer}")
    return True


async def mem():
    kernel = sk.Kernel()
    deployment, deployment_embedding, api_key, endpoint = os.environ.get("MODEL_NAME"), os.environ.get('MODEL_NAME_EMBEDDING'), os.environ.get("MODEL_API_KEY"), os.environ.get("MODEL_ENDPOINT")
    azure_chat_service = AzureChatCompletion(deployment_name=deployment, endpoint=endpoint, api_key=api_key)
    azure_text_embedding = AzureTextEmbedding(deployment_name=deployment_embedding, endpoint=endpoint, api_key=api_key)
    kernel.add_chat_service("chat_completion", azure_chat_service)
    kernel.add_text_embedding_generation_service("ada", azure_text_embedding)
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    kernel.import_plugin(sk.core_plugins.TextMemoryPlugin())

    print(Fore.MAGENTA+"Thanks for selecting Memories Demo")
    print(Fore.MAGENTA+"Manual Memories------------------------")
    
    print(Fore.LIGHTGREEN_EX)
    #Manually adding memories
    print("Populating memory...")
    await populate_memory(kernel,"aboutMe")
    print("Asking questions... (manually)")
    await search_memory_examples(kernel,"aboutMe")
    print("Setting up a chat (with memory!)")
    chat_func, context = await setup_chat_with_memory(kernel)
    print("Begin chatting (type 'exit' to exit):\n")
    chatting = True
    while chatting:
        chatting = await chat(kernel, chat_func, context)

    # Azure AI Search
    print(Fore.MAGENTA+"Using Azure AI Search------------------------")
    from semantic_kernel.connectors.memory.azure_cognitive_search import (AzureCognitiveSearchMemoryStore)
    azure_ai_search_api_key, azure_ai_search_url = os.environ.get("AI_API_KEY"), os.environ.get("AI_URL")

    # text-embedding-ada-002 uses a 1536-dimensional embedding vector
    kernel.register_memory_store(memory_store=AzureCognitiveSearchMemoryStore(vector_size=1536, search_endpoint=azure_ai_search_url, admin_key=azure_ai_search_api_key))

    print(Fore.LIGHTGREEN_EX)
    await populate_memory(kernel,"aboutMe")
    await search_memory_examples(kernel,"aboutMe")
    print(Fore.MAGENTA +"End of Memories Demo------------------------")

