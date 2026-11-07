from pathlib import Path

from expense_manager import (
    add_expense,
    search_expenses,
    delete_expense,
    calculate_summary
)

from storage import load_expenses, save_expenses
from import_export import import_records, export_records
from data_processor import process_records


def display_menu():
    print("\n========== EXPENSE MANAGEMENT SYSTEM ==========")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expenses")
    print("4. Delete Expense")
    print("5. View Summary")
    print("6. Exit")
    print("7. Import Expenses")
    print("8. Export Expenses")


def add_expense_menu(expenses):
    print("\n--- Add Expense ---")

    title = input("Enter title: ")
    amount = input("Enter amount: ")
    category = input("Enter category: ")

    expense_date = input(
        "Enter date (YYYY-MM-DD), or press Enter for today: "
    ).strip()

    if not expense_date:
        expense_date = None

    expense = add_expense(
        expenses, title, amount, category, expense_date
    )

    save_expenses(expenses)

    print(f"\nExpense added successfully. ID: {expense['id']}")


def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    for expense in expenses:
        print(
            f"ID: {expense['id']} | "
            f"Title: {expense['title']} | "
            f"Amount: ₹{expense['amount']:.2f} | "
            f"Category: {expense['category']} | "
            f"Date: {expense['date']}"
        )


def search_expenses_menu(expenses):
    search_term = input(
        "\nEnter title or category to search: "
    )

    results = search_expenses(expenses, search_term)

    if not results:
        print("No matching expenses found.")
        return

    for expense in results:
        print(
            f"ID: {expense['id']} | "
            f"{expense['title']} | "
            f"₹{expense['amount']:.2f} | "
            f"{expense['category']} | "
            f"{expense['date']}"
        )


def delete_expense_menu(expenses):
    try:
        expense_id = int(input("\nEnter expense ID to delete: "))

        deleted = delete_expense(expenses, expense_id)
        save_expenses(expenses)

        print(f"Deleted expense: {deleted['title']}")

    except ValueError as error:
        print(f"Error: {error}")


def view_summary(expenses):
    summary = calculate_summary(expenses)

    print("\n--- Expense Summary ---")
    print(f"Total expenses: {summary['count']}")
    print(f"Total spending: ₹{summary['total']:.2f}")

    print("\nCategory-wise spending:")

    if not summary["categories"]:
        print("No expenses to summarise.")
        return

    for category, amount in summary["categories"].items():
        print(f"{category}: ₹{amount:.2f}")


def import_expenses_menu(expenses):
    print("\n--- Import Expenses ---")

    file_path = input("Enter CSV/JSON file path: ").strip()

    records = import_records(file_path)
    result = process_records(records)

    print("\n--- Import Preview ---")
    print(f"Valid records: {result['valid_count']}")
    print(f"Rejected records: {result['rejected_count']}")

    for rejected in result["rejected_records"]:
        print(
            f"Row {rejected['row']}: "
            f"{rejected['reason']}"
        )

    if not result["valid_records"]:
        print("No valid records available to import.")
        return

    confirm = input(
        "\nImport valid records? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Import cancelled.")
        return

    existing_keys = {
        (
            item["title"].strip().lower(),
            float(item["amount"]),
            item["category"].strip().lower(),
            item["date"]
        )
        for item in expenses
    }

    imported_count = 0
    duplicate_count = 0

    for record in result["valid_records"]:
        duplicate_key = (
            record["title"].lower(),
            record["amount"],
            record["category"].lower(),
            record["date"]
        )

        if duplicate_key in existing_keys:
            duplicate_count += 1
            continue

        expense = add_expense(
            expenses,
            record["title"],
            record["amount"],
            record["category"],
            record["date"]
        )

        existing_keys.add(duplicate_key)
        imported_count += 1

    if imported_count:
        save_expenses(expenses)

    print("\n--- Import Result ---")
    print(f"Successfully imported: {imported_count}")
    print(f"Already existing: {duplicate_count}")
    print(f"Rejected during processing: {result['rejected_count']}")


def export_expenses_menu(expenses):
    print("\n--- Export Expenses ---")

    if not expenses:
        print("No expenses available to export.")
        return

    print("1. Export as JSON")
    print("2. Export as CSV")

    choice = input("Choose format: ").strip()

    if choice == "1":
        file_path = Path(__file__).resolve().parent / "exports" / "expenses.json"

    elif choice == "2":
        file_path = Path(__file__).resolve().parent / "exports" / "expenses.csv"

    else:
        print("Invalid export choice.")
        return

    exported_file = export_records(expenses, file_path)

    print(f"Export successful: {exported_file.resolve()}")


def main():
    try:
        expenses = load_expenses()

        while True:
            display_menu()

            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    add_expense_menu(expenses)

                elif choice == "2":
                    view_expenses(expenses)

                elif choice == "3":
                    search_expenses_menu(expenses)

                elif choice == "4":
                    delete_expense_menu(expenses)

                elif choice == "5":
                    view_summary(expenses)

                elif choice == "6":
                    print("Goodbye!")
                    break

                elif choice == "7":
                    import_expenses_menu(expenses)

                elif choice == "8":
                    export_expenses_menu(expenses)

                else:
                    print("Invalid choice.")

            except (ValueError, FileNotFoundError, OSError) as error:
                print(f"Error: {error}")

    except (ValueError, OSError) as error:
        print(f"Unable to start application: {error}")


if __name__ == "__main__":
    main()
