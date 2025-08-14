import json
import hashlib
from pathlib import Path
from datetime import datetime

USERS_FILE = Path("data") / "users.json"
DEFAULT_CATEGORIES = {
    "income": ["Salary", "Freelance", "Bonus", "Interest", "Other"], 
    "expense": ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Health", "Shopping", "Other"]
}


def generate_user_id(users: dict):
    existing_ids = [int(uid[1:]) for uid in users.keys() if uid.startswith('u')]
    next_id = max(existing_ids, default=0) + 1
    return f"u{next_id:03}"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}")
        return {}

    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ User file is empty or invalid. Resetting it.")
        USERS_FILE.write_text("{}")
        return {}


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def signup(username, password):
    users = load_users()

    for user in users.values():
        if user["username"] == username:
            return False

    user_id = generate_user_id(users)
    users[user_id] = {
        "username": username,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(), 
        "categories": DEFAULT_CATEGORIES.copy()  # default categories
    }
    save_users(users)
    return user_id


def login(username, password):
    users = load_users()

    for user_id, user in users.items():
        if user["username"] == username and user["password"] == hash_password(password):
            return user_id
    return None


# save or update categories part in users.json