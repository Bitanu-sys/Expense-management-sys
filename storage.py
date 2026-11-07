import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "expenses.json"

def load_expenses():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()

        if not content:
            return []

        try:
            return json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Expense data file contains invalid JSON."
            ) from error

def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)