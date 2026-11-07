
import csv
import json
from pathlib import Path



def import_records(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".json":
        with open(file_path, "r", encoding="utf-8") as file:
            records = json.load(file)

    elif extension == ".csv":
        with open(
            file_path, "r", encoding="utf-8-sig", newline=""
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV file has no header.")

            reader.fieldnames = [
                name.strip().lower()
                for name in reader.fieldnames
            ]

            records = [
                {
                    key.strip().lower(): value
                    for key, value in record.items()
                    if key is not None
                }
                for record in reader
            ]

    else:
        raise ValueError("Only CSV and JSON files are supported.")

    if not isinstance(records, list):
        raise ValueError("Imported data must contain a list of records.")

    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every record must be a dictionary.")

    return records


def export_records(records, file_path):
    file_path = Path(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    extension = file_path.suffix.lower()

    if extension == ".json":
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    elif extension == ".csv":
        if not records:
            raise ValueError("Cannot export an empty dataset to CSV.")

        fieldnames = list(records[0].keys())

        with open(
            file_path,
            "w",
            encoding="utf-8",
            newline=""
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(records)

    else:
        raise ValueError("Only CSV and JSON exports are supported.")

    return file_path
