import os
import json
from pathlib import Path

DATA_DIR = Path("data")  # base folder for JSON files

def get_transaction_file(user_id):
    return DATA_DIR / f"transactions_{user_id}.json"

def load_user_data(user_id):
    filepath = get_transaction_file(user_id)
    return load_data(filepath)

def save_user_data(user_id, transactions):
    filepath = get_transaction_file(user_id)
    save_data(filepath, transactions)

# Your existing logic — keep this as-is:
def load_data(filepath):
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            else:
                return {}

    except json.JSONDecodeError:
        print("⚠️ JSON file is empty or corrupted. Starting fresh.")
        return {}

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {}

def save_data(filepath, transactions):
    if not isinstance(transactions, dict):
        raise ValueError("Data must be a dictionary with transaction IDs as keys")

    with open(filepath, 'w') as file:
        json.dump(transactions, file, indent=4)
