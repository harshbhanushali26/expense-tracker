from utils.display import show_main_menu, print_section_title, print_error, print_success
from rich.prompt import Prompt
from menu.manage_menu import manage_main_menu
from menu.analysis_menu import analysis_main_menu
from menu.category_menu import manage_category_menu
from menu.export_menu import export_main_menu




def main_menu(manager, category_manager):
    
    while True: 
        print_section_title("Main Menu", "🛠️ ")
        show_main_menu()
        choice = Prompt.ask("\n👉 Select an option").strip()

        if choice == "1":
            manage_main_menu(manager, category_manager)
        elif choice == "2":
            analysis_main_menu(manager, category_manager)
        elif choice == "3":
            manage_category_menu(category_manager)
        elif choice == "4":
            export_main_menu(manager)
        elif choice == "0":
            print_success("Thank you for using Personal Expense Tracker! 👋")
            exit()
        else:
            print_error("Invalid choice. Please try again.")
            
            
if __name__ == "__main__":
    main_menu()

