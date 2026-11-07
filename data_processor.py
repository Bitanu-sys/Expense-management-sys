
from expense_manager import validate_expense


def process_records(records):
    valid_records = []
    rejected_records = []
    seen_records = set()

    for row_number, record in enumerate(records, start=1):

        try:
            cleaned = validate_expense(
                title=record.get("title", ""),
                amount=record.get("amount", ""),
                category=record.get("category", ""),
                expense_date=record.get("date", "")
            )

            duplicate_key = (
                cleaned["title"].lower(),
                cleaned["amount"],
                cleaned["category"].lower(),
                cleaned["date"]
            )

            if duplicate_key in seen_records:
                rejected_records.append({
                    "row": row_number,
                    "record": record,
                    "reason": "Duplicate record"
                })
                continue

            seen_records.add(duplicate_key)
            valid_records.append(cleaned)

        except ValueError as error:
            rejected_records.append({
                "row": row_number,
                "record": record,
                "reason": str(error)
            })

    return {
        "valid_records": valid_records,
        "rejected_records": rejected_records,
        "valid_count": len(valid_records),
        "rejected_count": len(rejected_records)
    }
