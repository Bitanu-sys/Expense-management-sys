from datetime import date, datetime


def validate_expense(title, amount, category, expense_date):
    title = title.strip()
    category = category.strip()

    if not title:
        raise ValueError("Title cannot be empty.")

    if not category:
        raise ValueError("Category cannot be empty.")

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must use YYYY-MM-DD format.")

    return {
        "title": title,
        "amount": amount,
        "category": category,
        "date": expense_date
    }


def add_expense(expenses, title, amount, category, expense_date=None):
    if expense_date is None:
        expense_date = date.today().isoformat()

    expense = validate_expense(
        title, amount, category, expense_date
    )

    new_id = max(
        (item["id"] for item in expenses),
        default=0
    ) + 1

    expense["id"] = new_id
    expenses.append(expense)

    return expense


def search_expenses(expenses, search_term):
    search_term = search_term.strip().lower()

    if not search_term:
        raise ValueError("Search term cannot be empty.")

    return [
        expense for expense in expenses
        if search_term in expense["title"].lower()
        or search_term in expense["category"].lower()
    ]


def delete_expense(expenses, expense_id):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            return expenses.pop(index)

    raise ValueError("Expense ID not found.")


def calculate_summary(expenses):
    total = sum(expense["amount"] for expense in expenses)

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense["amount"]
        )

    return {
        "total": total,
        "count": len(expenses),
        "categories": category_totals
    }