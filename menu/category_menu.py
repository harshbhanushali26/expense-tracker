from rich.prompt import Prompt
from utils.display import show_category_menu, print_error, print_success, print_section_title, console
from utils.validation import validate_type



def handle_add_category(category_manager):
    print_section_title("Add New Category", "➕", color="cyan")
    
    type = validate_type("Enter type (income/expense)", allow_blank=False)
    categories = category_manager.get_income_categories() if type == "income" else category_manager.get_expense_categories()
    category = ""
    while True:
        console.print(f"Available Categories | {', '.join(categories)}")
        category = Prompt.ask("Enter Category").strip()
        if category == "":
            print_error("Category cannot be empty!")
        else:
            success = category_manager.add_category(type, category)
            if success:
                print_success(f"Category '{category}' added successfully!")
                break
            else:
                print_error("Category already exist, Retry")
                
                
def handle_view_category(category_manager):
    print_section_title("View Categories", "📋", color="cyan")
    
    categories = category_manager.view_categories()
    
    print("\n💰 Income Categories:")
    for category in sorted(categories["income"]):
        console.print(f"[bold green]  • {category} [/bold green]")
    
    print("\n💸 Expense Categories:")
    for category in sorted(categories["expense"]):
        console.print(f"[bold yellow]  • {category} [/bold yellow]")
    
    print()  # Extra line for spacing


def manage_category_menu(category_manager): 
    actions = {
                "1": lambda: handle_add_category(category_manager),
                "2": lambda: handle_view_category(category_manager), 
                "0": lambda: None
            }
    
    
    while True:
        print_section_title("Manage Transactions", icon="📋  ")
        show_category_menu()
        
        choice = Prompt.ask("\n👉 Select an option")
        action = actions.get(choice)
        
        if choice == "0":
            break
            
        if action:
            action()
            input("\n[Press Enter to return to category menu...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    manage_category_menu()
        
        



