import uuid
from datetime import date, datetime 

class Transaction:
    def __init__(self, type, amount, category, date, id=None, description=None):
        self.id = id if id is not None else str(uuid.uuid4())   # Use the passed id if available, otherwise generate a new one
        self.type = type
        self.amount = amount
        self.category = category
        self.date = self.clean_date(date)
        self.description = description
        
    @staticmethod
    def clean_date(value):
        if isinstance(value, str):
            return value.strip()[:10]  # Always get YYYY-MM-DD
        elif isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        return str(value)[:10]


    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, transaction):
        return cls(
            type=transaction['type'],
            amount=transaction['amount'],
            category=transaction['category'],
            date=transaction['date'],
            id=transaction.get('id'),
            description=transaction.get('description')
        )

    def __str__(self):
        return (f"ID : {self.id}\n"
                f"Date : {self.date}\n"
                f"Type : {self.type}\n"
                f"Amount : {self.amount}\n"
                f"Category : {self.category}\n"
                f"Description : {self.description if self.description else 'N/A'}")
