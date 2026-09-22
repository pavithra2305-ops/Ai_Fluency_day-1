from expense_data import EXPENSES


def get_expense(category):
    return EXPENSES.get(category)


def get_total_expense():
    return sum(EXPENSES.values())


def get_highest_expense():
    category = max(EXPENSES, key=EXPENSES.get)
    return {
        "category": category,
        "amount": EXPENSES[category]
    }