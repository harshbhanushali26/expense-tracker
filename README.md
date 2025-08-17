# 📊 Expense Tracker CLI

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/harshbhanushali26/expense-tracker)](../../)
[![Issues](https://img.shields.io/github/issues/harshbhanushali26/expense-tracker)](../../issues)
[![Last Commit](https://img.shields.io/github/last-commit/harshbhanushali26/expense-tracker)](../../commits/main)

A simple **Python CLI app** to track income, expenses, and budgets with multi-user support.  
Stores data in **JSON files** and offers analytics, filtering, and a modular structure for easy upgrades.

---

## ✨ Features
- 🔑 Multi-user authentication (password hashing)
- ➕ Add, view, delete transactions (income/expense)
- ✏️ Create and manage custom categories
- 🗂 Categorized tracking with daily, monthly, and category breakdown
- 🔍 Advanced filtering by category, date range, type, month, exact date
- 📤 Export transactions to CSV, JSON, Excel, and PDF
- 💾 Persistent per-user JSON storage
- ⚙️ Modular, easy-to-extend design

---



## 📂 Project Structure
Expense-Tracker/
├── core/
│   ├── manager.py
│   ├── category.py
│   ├── transaction.py
│   └── export.py         
├── data/
│   ├── transactions_u001.json
│   ├── transactions_u002.json
│   └── users.json
├── menu/
│   ├── analysis_menu.py
│   ├── category_menu.py
│   ├── main_menu.py
│   ├── manage_menu.py
│   └── export_menu.py    integration
├── utils/
│   ├── auth.py
│   ├── init.py
│   ├── display.py
│   ├── filtering.py
│   ├── json_io.py
│   └── validation.py
├── .gitignore
├── main.py
└── README.md



---

## 🚀 Installation
```bash
# 1. Clone the repository
git clone https://github.com/harshbhanushali26
/expense-tracker.git
cd expense-tracker

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Run the app
python main.py
```

## 🔮 Future Enhancements

- 💾 Backup & restore
- 📈 Graphical dashboard
- ☁️ Cloud sync
- 💱 Multi-currency support
- ⏳ Scheduled reports
- 💰 Budget limits & budget vs actual analysis
- 🔄 Recurring transactions (auto add & due check)

## 🛠 Tech Stack

- Python 3.10+
- JSON for storage
- Rich for styled CLI output

## 📜 License
MIT License – You can use, modify, and distribute this project.



