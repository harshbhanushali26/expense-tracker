from datetime import datetime


def filter_by_criteria(transactions:dict, type=None, category=None, date=None, from_date=None, to_date=None, month=None):
    filtered_transactions = transactions
    
    if type:
        filtered_transactions = filter_by_type(transactions, type)

    if category:
        filtered_transactions = filter_by_category(filtered_transactions, category)

    if date:
        filtered_transactions = filter_by_date(filtered_transactions, date)
        
    elif from_date and to_date:  # Only apply date range if exact date is not specified
        filtered_transactions = filter_by_date_range(filtered_transactions, from_date, to_date)
    
    elif month:  # Only apply month filter if no date filters are applied
        filtered_transactions = filter_by_month(filtered_transactions, month)


    return filtered_transactions



def filter_by_type(transactions, transaction_type):
    return {key : txn for key, txn in transactions.items() if txn.type == transaction_type}


def filter_by_category(transactions, category):
    return {key : txn for key, txn in transactions.items() if txn.category == category}


def filter_by_date(transactions, date):
    return {key : txn for key, txn in transactions.items() if txn.date == date}


def filter_by_month(transactions, month):
    return {key : txn for key, txn in transactions.items() if txn.date.startswith(month)}


def filter_by_date_range(transactions, from_date, to_date):
    # Convert string dates to datetime objects
    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")
    
    return {
        key: txn for key, txn in transactions.items() 
        if start_date <= datetime.strptime(txn.date, "%Y-%m-%d") <= end_date
    }



