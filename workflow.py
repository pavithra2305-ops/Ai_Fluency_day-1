from expense_data import EXPENSES


def workflow(question):
    question = question.lower()

    # Rule 1: Food spending
    if "food" in question:
        return f"You spent ₹{EXPENSES['Food']} on Food."

    # Rule 2: Total spending
    elif "total" in question:
        total = sum(EXPENSES.values())
        return f"Your total spending is ₹{total}."

    # Rule 3: Highest spending category
    elif "highest" in question:
        category = max(EXPENSES, key=EXPENSES.get)
        amount = EXPENSES[category]
        return f"Your highest spending is on {category}: ₹{amount}."

    # If no rule matches
    else:
        return "Sorry, I don't have a rule for this question."


if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW ===\n")

    questions = [
        "How much did I spend on food?",
        "What is my total spending?",
        "Which category has the highest spending?"
    ]

    for question in questions:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)