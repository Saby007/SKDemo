from colorama import Fore, Style, init
import Prompt_Engineering.pe_basic as peb
import Prompt_Engineering.pe_specific as pes
import Prompt_Engineering.pe_structure_output as peso
import Prompt_Engineering.pe_few_shot as pefs
import Prompt_Engineering.pe_go_wrong as pegw
import Prompt_Engineering.pe_provide_context as pepc
import Prompt_Engineering.pe_variables as pev
import Prompt_Engineering.pe_nested_function as penf
import Prompt_Engineering.pe_final_example as pefe

async def pe():
    print(Fore.YELLOW + "Thanks for selecting prompt engineering Demo")
    while(True):
        print(Fore.YELLOW+"Which Topic you want to explore now?")
        print(Fore.YELLOW+"1. Prompt Engineering - Basic")
        print(Fore.YELLOW+"2. Prompt Engineering - More Specific")
        print(Fore.YELLOW+"3. Prompt Engineering - Add Structure to the Output")
        print(Fore.YELLOW+"4. Prompt Engineering - Few Shot Learning")
        print(Fore.YELLOW+"5. Prompt Engineering - Guidance when things go wrong")
        print(Fore.YELLOW+"6. Prompt Engineering - Provide context")
        print(Fore.YELLOW+"7. Prompt Engineering - Variables")
        print(Fore.YELLOW+"8. Prompt Engineering - Nested Functions")
        print(Fore.YELLOW+"9. Prompt Engineering - Final Prompt Engineering Example")
        print(Fore.YELLOW+"10. Back to Menu")
        print(Fore.YELLOW+"11. Exit")
        choice = int(input(Fore.WHITE+"Enter your choice: "))
        if(choice == 1):
            await peb.pe_basic()
        elif(choice == 2):
            await pes.pe_specific()
        elif(choice == 3):
            await peso.pe_structure_output()
        elif(choice == 4):
            await pefs.pe_few_shot()
        elif(choice == 5):
            await pegw.pe_go_wrong()
        elif(choice == 6):
            await pepc.pe_provide_context()
        elif(choice == 7):
            await pev.pe_variables()
        elif(choice == 8):
            await penf.pe_nested_function()
        elif(choice == 9):
            await pefe.pe_final_example()
        elif(choice == 10):
            print(Fore.YELLOW+"Thank you for exploring the Prompt Engineering Demo in Python!!!")
            break
        elif(choice == 11):
            print(Fore.YELLOW+"Thank you for exploring the Prompt Engineering Demo in Python!!!")
            exit()


    