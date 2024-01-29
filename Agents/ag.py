from colorama import Fore, Style, init
from Agents import ag_out_of_box as agobo
from Agents import ag_semantic_function as agsf
from Agents import ag_native_function as agnf
from Agents import ag_planner as agpl

async def ag():
    print(Fore.YELLOW + "Thanks for selecting Agents Demo")
    while(True):
        print(Fore.YELLOW+"Which Topic you want to explore now?")
        print(Fore.YELLOW+"1. Agents - Semantic Function Plugin")
        print(Fore.YELLOW+"2. Agents - Native Function Plugin")
        print(Fore.YELLOW+"3. Agents - Out of the Box Plugin")
        print(Fore.YELLOW+"4. Agents - Planner")
        print(Fore.YELLOW+"5. Back to Menu")
        print(Fore.YELLOW+"6. Exit")
        choice = int(input(Fore.WHITE+"Enter your choice: "))
        if(choice == 1):
            await agsf.ag_semantic_function()
        elif(choice == 2):
            await agnf.ag_native_function()
        elif(choice == 3):
            await agobo.ag_out_of_box()
        elif(choice == 4):
            await agpl.ag_planner()
        elif(choice == 5):
            print(Fore.YELLOW+"Thank you for exploring the Agents Demo in Python!!!")
            break
        elif(choice == 6):
            print(Fore.YELLOW+"Thank you for exploring the Agents Demo in Python!!!")
            exit()


    