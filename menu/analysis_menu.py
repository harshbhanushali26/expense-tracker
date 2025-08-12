from utils.validation import validate_date, validate_type
from rich.prompt import Prompt
from utils.display import print_section_title, print_warning, console, display_summary, Table, datetime, box, show_analysis_menu, print_error, print_txn_table, print_success
from utils.filtering import filter_by_criteria, filter_by_month
from utils.validation import validate_type, validate_category, validate_date
from utils.categories import get_expense_categories, get_income_categories



def handle_daily_summary(manager):
    print_section_title("Daily Summary", "📆", color="cyan")
    date = validate_date("Enter date (YYYY-MM-DD): ")
    
    console.print(" ")
    summary = manager.get_daily_summary(date)
    is_today = datetime.now().strftime("%Y-%m-%d") == date

    display_summary(summary, f"📆 Summary for {date}", is_today=is_today, period_label="day")


def handle_monthly_summary(manager):
    print_section_title("Monthly Summary", "📅", color="cyan")
    month = Prompt.ask("Enter month (YYYY-MM)")
    summary = manager.get_monthly_summary(month)
    
    display_summary(summary, f"📅 Summary for {month}", is_today=False, period_label="month")


def handle_category_breakdown(manager):
    
    console.print("\n[bold cyan]📊 Category Breakdown[/bold cyan]\n")
    
    txn_list = handle_filter(manager, filter_usage="category breakdown")
    
        
    type = validate_type("Enter type (income/expense)")
    breakdown = get_category_breakdown(type, txn_list)
        
    if not breakdown:
        print_warning("No data found for the selected type.")
        return

    table = Table(title=f"{type.capitalize()} Breakdown", show_header=True, header_style="magenta", box=box.SIMPLE_HEAVY)
    table.add_column("Category")
    table.add_column("Total Amount", justify="right")

    for category, total in breakdown.items():
        table.add_row(category, str(total))

    console.print(table)


def sort_transactions(transactions, sort_by="date", order="asc"):
    """
    Sort transactions by date or amount
    
    Args:
        transactions: Dict of {transaction_id: transaction_object}
        sort_by: "date" or "amount"
        order: "asc" or "desc"
    
    Returns:
        List of sorted transaction objects (values only)
    """
    try:
        # Convert dict values to list for sorting
        txn_list = list(transactions.values())
        
        if sort_by == "date":
            sorted_txns = sorted(
                txn_list, 
                key=lambda txn: datetime.strptime(txn.date, "%Y-%m-%d"),
                reverse=(order == "desc")
            )
        elif sort_by == "amount":
            sorted_txns = sorted(
                txn_list,
                key=lambda txn: float(txn.amount),
                reverse=(order == "desc")
            )
        else:
            print_warning(f"Invalid sort option: {sort_by}")
            return txn_list
        
        return sorted_txns
        
    except Exception as e:
        print_warning(f"Error sorting transactions: {e}")
        return list(transactions.values())


def get_sort_choice():
    """
    Get sorting preference from user
    
    Returns:
        tuple: (sort_by, order) or (None, None) if no sorting
    """
    console.print(f"\n[bold yellow]Sort Options[/bold yellow]")
    sort_by = Prompt.ask("Sort by", choices=["date", "amount", "none"], default="none")
    
    if sort_by == "none":
        return None, None
    
    order = Prompt.ask("Order", choices=["asc", "desc"], default="asc")
    return sort_by, order


def handle_filter(manager, filter_usage=None):
    
    type_filter = category_filter = None
    date_filter = from_date = to_date = month_filter = None
    current_month = datetime.now().strftime("%Y-%m")
    
    
    # only date filters and sort by amount only if possible
    console.print("Press [bold green]Enter[/bold green] to for current month category wise breakdown or apply custom filters")
    apply_filters = Prompt.ask("Apply filters?", choices=["yes", "no"], default="no").lower().strip()
    
    if apply_filters == "no":
        # Default: current month
        month_filter = current_month
        transactions = filter_by_month(manager.transactions, month_filter)
        filter_summary = f"Month: {month_filter}"
    else:
        
        # Step 2: Ask for date filters first
        console.print(f"\n[bold yellow]Date Filters[/bold yellow]")
        date_filter_choice = Prompt.ask(
            "Apply date filter?", 
            choices=["exact", "range", "month", "no"], 
            default="no"
        )
        
        if date_filter_choice == "exact":
            date_filter = validate_date("Enter exact date (YYYY-MM-DD)", allow_blank=False)
            
        elif date_filter_choice == "range":
            from_date = validate_date("From date (YYYY-MM-DD)", allow_blank=False)
            to_date = validate_date("To date (YYYY-MM-DD)", allow_blank=False)
        
        elif date_filter_choice == "month":
            month_filter = Prompt.ask("Enter month (YYYY-MM)", default=current_month)
    
            
        if filter_usage == "category breakdown":
            # Apply all filters
            transactions = filter_by_criteria(
                manager.transactions, 
                type=None, 
                category=None,
                date=date_filter, 
                from_date=from_date, 
                to_date=to_date, 
                month=month_filter
            )
            
            transactions = filter_by_criteria(
            manager.transactions, 
            type=type_filter, 
            category=category_filter,
            date=date_filter, 
            from_date=from_date, 
            to_date=to_date, 
            month=month_filter
        )
    
            filters_applied = []
            if date_filter: filters_applied.append(f"Date: {date_filter}")
            elif from_date and to_date: filters_applied.append(f"Range: {from_date} to {to_date}")
            elif month_filter: filters_applied.append(f"Month: {month_filter}")
            
            filter_summary = " | ".join(filters_applied) if filters_applied else "No filters"
            
        else:
            # Step 3: Ask for type and category filters
            console.print(f"\n[bold yellow]Other Filters[/bold yellow]")
            type_filter = validate_type("Enter Type (income/expense or press Enter to skip)", allow_blank=True)
            
            if type_filter:
                categories = get_income_categories() if type_filter == "income" else get_expense_categories()
                category_filter = validate_category(
                    f"Enter category (or press Enter to skip) - ({', '.join(categories)})", 
                    categories, allow_blank=True
                )
            
            transactions = filter_by_criteria(
            manager.transactions, 
            type=type_filter, 
            category=category_filter,
            date=date_filter, 
            from_date=from_date, 
            to_date=to_date, 
            month=month_filter
                )
    
            filters_applied = []
            if type_filter: filters_applied.append(f"Type: {type_filter}")
            if category_filter: filters_applied.append(f"Category: {category_filter}")
            if date_filter: filters_applied.append(f"Date: {date_filter}")
            elif from_date and to_date: filters_applied.append(f"Range: {from_date} to {to_date}")
            elif month_filter: filters_applied.append(f"Month: {month_filter}")
            
            filter_summary = " | ".join(filters_applied) if filters_applied else "No filters"
    
    
    if not transactions:
        print_warning("No transactions found with applied filters.")
        return
    
    # Show initial results
    txn_list = list(transactions.values())
    console.print(f"\n[bold green]📋 Applied Filters: {filter_summary}[/bold green]")
    print_success(f"[green]Found {len(transactions.values()  )} transactions[/green]")

    if filter_usage == "category breakdown":
        return txn_list    
        
    else:
        # Get sorting choice
        sort_by, order = get_sort_choice()

        if sort_by:
            # Pass the dict, get back sorted list
            txn_list = sort_transactions(transactions, sort_by, order)
            
            order_text = "ascending ↑" if order == "asc" else "descending ↓"
            console.print(f"\n[bold cyan]📈 Results sorted by {sort_by} ({order_text}):[/bold cyan]")
        else:
            txn_list = list(transactions.values())
            console.print(f"\n[bold cyan]📋 Results:[/bold cyan]")
            
        print_txn_table(txn_list)


def get_category_breakdown(type_, txns):
    category_wise_summary = {}
    
    for txn in txns:
        if txn.type == type_:
            category = txn.category
            amount = txn.amount

            if category in category_wise_summary:
                category_wise_summary[category] += amount
            else:
                category_wise_summary[category] = amount

    return category_wise_summary



def analysis_main_menu(manager):
    
    actions = {
        "1": lambda: handle_daily_summary(manager),
        "2": lambda: handle_monthly_summary(manager),
        "3": lambda: handle_category_breakdown(manager),
        "4": lambda: handle_filter(manager, filter_usage=""),
        "0": lambda: None
        }
    
    
    while True:
        print_section_title("Analysis", icon="📊 ")
        show_analysis_menu()
        
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
    analysis_main_menu()