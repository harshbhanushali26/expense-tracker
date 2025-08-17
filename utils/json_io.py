import os
import json
from pathlib import Path
from utils.auth import load_users, save_users

DATA_DIR = Path("data")  # base folder for JSON files
USERS_FILE = Path("data") / "users.json"


# get loggined user txn file
def get_transaction_file(user_id):
    return DATA_DIR / f"transactions_{user_id}.json"


# gets user file and call load data
def load_user_data(user_id):
    filepath = get_transaction_file(user_id)
    return load_data(filepath)


# gets user file and call save data
def save_user_data(user_id, transactions):
    filepath = get_transaction_file(user_id)
    save_data(filepath, transactions)


# loads data from file 
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


# save data to file
def save_data(filepath, transactions):
    if not isinstance(transactions, dict):
        raise ValueError("Data must be a dictionary with transaction IDs as keys")

    with open(filepath, 'w') as file:
        json.dump(transactions, file, indent=4)


# loading user info for categories
def load_user_info(user_id):
    try:
        with open(USERS_FILE, 'r') as file:
            data = json.load(file)
            return data.get(user_id)  # Returns user data or None if not found
    except FileNotFoundError:
        return None 
    except json.JSONDecodeError:
        return None  


# saving user info for categories
def save_user_info(user_id, categories):
    try:
        users = load_users()
        if user_id in users:
            users[user_id]['categories'] = categories
            save_users(users)
        else:
            raise ValueError(f"User {user_id} not found")
    except Exception as e:
        print(f"Error saving categories: {e}")
        return False
    return True