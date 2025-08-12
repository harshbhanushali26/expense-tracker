import sys
from rich.prompt import Prompt
from core.manager import ExpenseManager
from utils.json_io import get_transaction_file
from utils.auth import login, signup
from utils.display import print_header, print_success, print_warning, print_error, console, show_dashboard
from datetime import datetime, date
from menu.main_menu import main_menu




def handle_show_dashboard(manager, user_name):
    today_date = date.today()
    current_year_month = datetime.today().strftime("%Y-%m")
    today_summary = manager.get_daily_summary(today_date.strftime("%Y-%m-%d"))
    month_summary = manager.get_monthly_summary(current_year_month)
    top_categories = manager.get_top_categories(current_year_month, 5)
    
    show_dashboard(today_summary, month_summary, top_categories, user_name)
  
    
def handle_login_option():
    while True:
        username = input("👤  Username: ").strip()
        password = input("🔒  Password: ").strip()
        user_id = login(username, password)
        if user_id:
            print_success(f"Welcome back, {username}!")
            current_user_id = user_id
            manager = ExpenseManager(f"data/transactions_{user_id}.json")
            manager.load_transactions()
            return username, current_user_id  
        else:
            print_error("Invalid credentials. Try again.\n")
            quit = Prompt.ask("Type 'q' to quit else leave Blank", show_default="True", default="").strip().lower()
            
            if quit == 'q':
                sys.exit("👋 Exiting. See you soon!")
   
        
def handle_signup_option():
    while True:
        username = input("👤  Choose a username: ").strip()
        password = input("🔒  Choose a password: ").strip()
        if signup(username, password):
            print_success("🎉 Signup successful! You can now log in.\n")
        else:
            print_warning("⚠️ Username already taken. Try a different one.\n")
            quit = Prompt.ask("Type 'q' to quit else leave Blank", show_default="True", default="").strip().lower()
            
            if quit == 'q':
                sys.exit("👋 Exiting. See you soon!")



def main():
    print_header()
    
    current_user_id = None
    while current_user_id is None:
        
        console.print("[bold cyan]1.[/bold cyan] 🪪   Login")
        console.print("[bold cyan]2.[/bold cyan] 🔐  Signup")
        console.print("[bold cyan]0.[/bold cyan] 🔚  Exit")
        
        choice = Prompt.ask("\n👉 Select an option").strip()

        if choice == "1":
            username, current_user_id = handle_login_option()
        elif choice == "2":
            handle_signup_option()
        elif choice == "0":
            print_success("Thank you for using Personal Expense Tracker! 👋")
            return
        else:
            print_error("❗ Invalid choice. Please enter 1, 2, or 3.\n")
            
    user_filepath = get_transaction_file(current_user_id)
    manager = ExpenseManager(filepath=user_filepath)
            
    handle_show_dashboard(manager, username)
    main_menu(manager)
            


if __name__ == "__main__":
    main()
