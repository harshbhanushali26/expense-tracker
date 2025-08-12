from core.transaction import Transaction
from utils.json_io import load_data, save_data
from utils.filtering import filter_by_criteria
from datetime import datetime,date
from collections import defaultdict


class ExpenseManager:
    def __init__(self, filepath):
        self.transactions = {}
        self.filepath = filepath
        self.load_transactions()


    def load_transactions(self):
        raw_data = load_data(self.filepath)     # from utils
        self.transactions = {txn_id : Transaction.from_dict(data) for txn_id, data in raw_data.items()}
        return self.transactions
    

    def save_transactions(self):
        transactions_dict = {
            txn_id: txn.to_dict() for txn_id, txn in self.transactions.items()
        }
        save_data(self.filepath, transactions_dict)    # from utils


    def add_transaction(self, transaction: Transaction):
        # Checking and adding to dictionary
        if not isinstance(transaction, Transaction):
            raise ValueError("Must be a Transaction instance")
        
        if transaction.id in self.transactions:
            return False
        
        self.transactions[transaction.id] = transaction
        self.save_transactions()
        return True


    def update_transaction(self, txn_id:str, updated_fields):   # updated_fields = {} dictionary of fields to change
        
        if txn_id not in self.transactions:
            return False
        
        transaction = self.transactions[txn_id]
        allowed_fields = {"amount", "category", "description", "date", "type"}

        for key, value in updated_fields.items():
            if key in allowed_fields and value is not None:
                setattr(transaction, key, value)

        self.save_transactions()
        return True
        

    def delete_transaction(self, txn_id:str):
        if txn_id not in self.transactions:
            return False
        
        del self.transactions[txn_id]
        self.save_transactions()
        return True
    


    def get_daily_summary(self, date):
        summary = {}
        num_income = 0
        num_expense = 0
        total_income = 0
        total_expense = 0
        category_breakdown = defaultdict(float)
        
        transactions = filter_by_criteria(self.transactions, date=date)
        for txn in transactions.values():
            if txn.type == 'income':
                total_income += txn.amount
                num_income += 1
            else:
                total_expense += txn.amount
                category_breakdown[txn.category] += txn.amount
                num_expense += 1

        summary['income'] = total_income
        summary['expense'] = total_expense
        summary["carry_forward"] = self._calculate_carry_forward(date)
        summary['balance'] = total_income - total_expense
        summary['num_income'] = num_income
        summary['num_expense'] = num_expense
        summary['breakdown'] = dict(category_breakdown)

        return summary
    

    def get_monthly_summary(self, month):
        summary = {}
        num_income = 0
        num_expense = 0
        total_income = 0
        total_expense = 0
        category_breakdown = defaultdict(float)
        
        transactions = filter_by_criteria(self.transactions, month=month)
        
        for txn in transactions.values():
            if txn.type == 'income':
                total_income += txn.amount
                num_income += 1
            else:
                total_expense += txn.amount
                category_breakdown[txn.category] += txn.amount
                num_expense += 1

        first_day_of_month = f"{month}-01"
        carry_forward = self._calculate_carry_forward(first_day_of_month)

        summary['income'] = total_income
        summary['expense'] = total_expense
        summary['carry_forward'] = carry_forward
        summary['balance'] = total_income - total_expense
        summary['num_income'] = num_income
        summary['num_expense'] = num_expense
        summary['breakdown'] = dict(category_breakdown)

        return summary
    

    def get_category_breakdown(self, type_):
        category_wise_summary = {}
        
        for txn in self.transactions.values():
            if txn.type == type_:
                category = txn.category
                amount = txn.amount

                if category in category_wise_summary:
                    category_wise_summary[category] += amount
                else:
                    category_wise_summary[category] = amount

        return category_wise_summary


    def _calculate_carry_forward(self, date_str):

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        carry_forward = 0.0

        for txn in self.transactions.values():

            try:
                txn_date = datetime.strptime(txn.date, "%Y-%m-%d").date()
            except ValueError:
                continue  # Skip invalid date entries
            if txn_date < target_date:
                if txn.type == "income":
                    carry_forward += txn.amount
                elif txn.type == "expense":
                    carry_forward -= txn.amount

        return carry_forward
            
              
    def get_top_categories(self, month:str, top_n: int = 5) -> list:
        txns = self.get_monthly_transactions(month)  
        category_totals = defaultdict(float)

        for txn in txns:
            if txn.type == "expense":
                category_totals[txn.category] += txn.amount
                    
        sorted_totals = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        return sorted_totals[:top_n]


    def get_monthly_transactions(self, month: str):
        monthly_txns = []
        for txn in self.transactions.values():

            txn_date_str = txn.date.strftime("%Y-%m") if isinstance(txn.date, (date, datetime)) else txn.date

            if txn_date_str.startswith(month):
                monthly_txns.append(txn)

        return monthly_txns

