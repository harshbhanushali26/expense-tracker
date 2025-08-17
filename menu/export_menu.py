from utils.display import print_section_title, print_error, show_export_menu, datetime
from utils.validation import validate_date
from utils.filtering import filter_by_criteria
from rich.prompt import Prompt
from core.transaction import Transaction
import os
from core.export import Exporter


# creates filename on the basis of filter and timestamp
def get_export_filename(data_type: str, filter_type: str, filter_value: str, extension: str, base_dir="exports"):
    
    os.makedirs(base_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Build file name
    filename = f"export_{data_type}_{filter_type}_{filter_value}_{timestamp}.{extension}"
    return os.path.join(base_dir, filename)


# asking user for what type of data  user want
def get_export_data(manager):
    """
    Ask user for export filters (time + type), apply them, and return transactions + metadata.
    """
    type_option = date_option = filter_value = ""
    month_filter = from_date = to_date = None

    # --- Time filter ---
    while True:
        date_option = Prompt.ask("Choose time filter", choices=["range", "month", "all"]).strip()
        
        if date_option == "month":
            while True:
                month_filter = Prompt.ask("Enter month (YYYY-MM)").strip()
                if month_filter == "":
                    print_error("Month cannot be empty")
                else:
                    filter_value = month_filter
                    break
            break
        elif date_option == "range":
            from_date = validate_date("From date (YYYY-MM-DD)", allow_blank=False)
            to_date = validate_date("To date (YYYY-MM-DD)", allow_blank=False)
            filter_value = f"{from_date}_to_{to_date}"
            break
        elif date_option == "all":
            filter_value = "all"
            break
        else:
            print_error("Invalid option, Try again!")
    
    # --- Type filter ---
    while True:
        type_option = Prompt.ask("What do you want to export?", choices=["income", "expense", "both"]).strip()
        if type_option in ["income", "expense", "both"]:
            break
        print_error("Invalid option, Try again!")
    
    # --- Apply filters ---
    export_transactions = filter_by_criteria(
        manager.transactions,
        type=None if type_option == "both" else type_option,
        category=None,
        from_date=from_date,
        to_date=to_date,
        month=month_filter
    )

    return export_transactions, type_option, date_option, filter_value


# exports data and file 
def handle_export(manager, extension: str):
    export_transactions, type_option, date_option, filter_value = get_export_data(manager)

    if not export_transactions:
        print_error("No transactions found for the selected filters.")
        return
    

    filename = get_export_filename(type_option, date_option, filter_value, extension)
    data = [txn.to_dict() for txn in export_transactions.values()]
    
    if extension == "csv":
        Exporter.export_csv(data, filename)
    elif extension == "xlsx":
        Exporter.export_excel(data, filename)
    elif extension == "pdf":
        Exporter.export_pdf(data, filename)
    elif extension == "json":
        Exporter.export_json(data, filename)
    

    print(f"✅ Export complete! File saved at: {filename}")


def export_main_menu(manager):
    actions = {
        "1": lambda: handle_export(manager, "csv"),
        "2": lambda: handle_export(manager, "xlsx"),
        "3": lambda: handle_export(manager, "pdf"),
        "4": lambda: handle_export(manager, "json"),
        "0": lambda: None,
    }
    
    while True:
        print_section_title("Export", icon="📊 ")
        show_export_menu()
        
        choice = Prompt.ask("\n👉 Select an option")
        action = actions.get(choice)
        
        if choice == "0":
            break
            
        if action:
            action()
            input("\n[Press Enter to return to export menu...]")
        else:
            print_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    export_main_menu()