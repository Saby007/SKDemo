#----------------------------------------------------------------------------------------------------
# Created by: Sabyasachi Samaddar
# Created on: 25-01-2024
# Created for: Semantic Kernel Demo 
# Description: This is the main app file for the Semantic Kernel Demo in Python
# Topics covered:
# 1. Prompt Engineering
# 2. AI Agents
#   - Plugins
#       - Native Functions
#       - Out-of-the-box Plugins
#   - Planners
# 3. Memories   
# Referrences: 
# https://www.promptingguide.ai/introduction/basics
# https://learn.microsoft.com/en-us/semantic-kernel/prompts/your-first-prompt?tabs=python
# https://github.com/microsoft/semantic-kernel/tree/main/python
#----------------------------------------------------------------------------------------------------     

# Importing the SK Prerequisite
# pip install semantic-kernel
# versions semantic-kernel==0.4.7.dev0, openai==1.9.0, python==3.12.1
# Importing Libraries
from colorama import Fore, Style, init
import asyncio
from dotenv import load_dotenv
import logging
logging.getLogger('aiohttp').setLevel(logging.ERROR)

async def main():
    print(Fore.GREEN +"Welcome to the Semantic Kernel Demo in Python!!!")
    while(True):        
        print(Fore.GREEN +"Which Topic you want to explore now?")
        print(Fore.GREEN +"1. Prompt Engineering")
        print(Fore.GREEN +"2. AI Agents")
        print(Fore.GREEN +"3. Memories")
        print(Fore.GREEN +"4. Exit")
        choice = int(input(Fore.WHITE +"Enter your choice: "))
        if(choice == 1):
            import Prompt_Engineering.pe as pe
            await pe.pe()
        elif(choice == 2):
            import Agents.ag as ag
            await ag.ag()
        elif(choice == 3):
            import Memories.mem as mem
            await mem.mem()            
        elif(choice == 4):
            print(Fore.GREEN +"Thank you for exploring the Semantic Kernel Demo in Python!!!")
            break

if __name__ == "__main__":
    #Load environment variables from .env file
    load_dotenv()
    asyncio.run(main())
