from utils.validation import validate_amount,validate_category,validate_date,validate_description,validate_type
from utils.categories import get_expense_categories, get_income_categories
from core.transaction import Transaction
from rich.prompt import Prompt
from utils.display import print_section_title, print_success, print_warning, print_error, console, show_transaction_menu
from menu.analysis_menu import handle_filter



def handle_add_transaction(manager):
    print_section_title("Add New Transaction", "➕", color="cyan")
    
    type = validate_type("Enter type (income/expense): ", allow_blank=False)
    amount = validate_amount("Enter amount: ", allow_blank=False)
    categories = get_income_categories() if type == "income" else get_expense_categories()
    category = validate_category(f"Enter category ({', '.join(categories)}): ", categories, allow_blank=False)
    txn_date = validate_date("Enter date (YYYY-MM-DD): ", allow_blank=False)
    description = validate_description("Enter description (optional): ", allow_blank=True)

    transaction = Transaction(type, amount, category, txn_date, description=description)
    success = manager.add_transaction(transaction)
    if success:
        print_success("Transaction added successfully!")
    else:
        print_error("Failed to add transaction!")


def handle_update_transaction(manager):
    print_section_title("Update Transaction", "✏️ ", color="cyan")
    
    ask = Prompt.ask("Want to search for a transaction before selecting one? (y/n)").strip().lower()
    if ask in ['yes', 'y' ]:
        handle_filter(manager)
        
    txn_id = Prompt.ask("Enter the Transaction ID to update")

    if txn_id not in manager.transactions:
        print_error("Transaction ID not found.")
        return

    current_txn = manager.transactions[txn_id]
    console.print("[dim]Press Enter to skip any field you don't want to change.[/dim]")

    new_type = validate_type("Enter new type (income/expense): ", allow_blank=True)
    new_amount = validate_amount("Enter new amount: ", allow_blank=True)

    if new_type:
        categories = get_income_categories() if new_type == "income" else get_expense_categories()
    else:
        categories = get_income_categories() if current_txn.type == "income" else get_expense_categories()

    new_category = validate_category(f"Enter new category ({', '.join(categories)}): ", categories, allow_blank=True)
    new_date = validate_date("Enter new date (YYYY-MM-DD): ", allow_blank=True)
    new_desc = validate_description("Enter new description: ", allow_blank=True)

    updated_fields = {
        "type": new_type,
        "amount": new_amount,
        "category": new_category,
        "date": new_date,
        "description": new_desc
    }

    # Remove any fields that are still None (i.e., user skipped them)
    updated_fields = {k: v for k, v in updated_fields.items() if v is not None}

    if not updated_fields:
        print_warning("No fields were updated.")
        return
    
    confirm = input(f"Are you sure you want to update txn '{txn_id}'? (y/n): ").lower().strip()
    if confirm in ['n', "no"]:
        print_warning("Cancelled txn updation.")
        return

    success = manager.update_transaction(txn_id, updated_fields)
    if success:
        print_success("Transaction updated successfully!")
    else:
        print_error("Failed to update transaction!")


def handle_delete_transaction(manager):
    print_section_title("Delete Transaction", "🗑️ ", color="cyan")
    
    ask = Prompt.ask("Want to search for a transaction before selecting one? (y/n)").strip().lower()
    if ask in ['yes', 'y' ]:
        handle_filter(manager)
    
    txn_id = Prompt.ask("Enter the Transaction ID to delete")
    
    confirm = input(f"Are you sure you want to update txn '{txn_id}'? (y/n): ").lower().strip()
    if confirm in ['n', 'no']:
        print_warning("Cancelled txn deletion.")
        return
    
    success = manager.delete_transaction(txn_id)
    if success:
        print_success("Transaction deleted successfully!")
    else:
        print_error("Transaction ID not found!")


def handle_exit():
    return


def manage_main_menu(manager): 
    actions = {
                "1": lambda: handle_add_transaction(manager),
                "2": lambda: handle_update_transaction(manager),
                "3": lambda: handle_delete_transaction(manager),
                "0": lambda: None
            }
    
    
    while True:
        print_section_title("Manage Transactions", icon="⚙️  ")
        show_transaction_menu()
        
        choice = Prompt.ask("\n👉 Select an option")
        action = actions.get(choice)
        
        if choice == "0":
            break
            
        if action:
            action()
            input("\n[Press Enter to return to main menu...]")  # ⏸️ Pause after action
        else:
            print_error("Invalid choice. Please try again.")

if __name__ == "__main__":
    manage_main_menu()
        
        