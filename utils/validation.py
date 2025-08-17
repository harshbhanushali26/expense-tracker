from datetime import datetime
from rich.prompt import Prompt
from utils.display import print_error


def validate_amount(prompt, allow_blank=True):
    while True:
        try:
            value = float(Prompt.ask(prompt).strip())

            if allow_blank and value == "":
                return None  # user skipped

            if value > 0:
                return value
            print_error("Amount must be greater than 0.")
        except ValueError:
            print_error("Please enter a valid number.")
            

def validate_type(prompt, allow_blank=True):
    while True:
        value = Prompt.ask(prompt).strip().lower()
        if allow_blank and value == "":
            return None  # user skipped

        if value in ("income", "expense"):
            return value
        print_error("Type must be 'income' or 'expense'.")
        

def validate_date(prompt, allow_blank=True):
    while True:
        value = Prompt.ask(prompt).strip()
        if allow_blank and value == "":
            return None  # user skipped

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print_error("Date must be in YYYY-MM-DD format.")


def validate_category(prompt, category_list, allow_blank=True):
    while True:
        value = Prompt.ask(prompt, show_default=True).strip()
        if allow_blank and value == "":
            return None  # user skipped
        
        if value == "new":
            return value

        if value in category_list:
            return value
        print_error(f"Invalid category. Choose from: {', '.join(category_list)}")


def validate_description(prompt, allow_blank=True):
    value = Prompt.ask(prompt).strip()
    if allow_blank and value == "":
            return None  # user skipped

    return value if value else None
