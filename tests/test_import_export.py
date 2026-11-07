
import json
import pytest

from import_export import import_records, export_records


@pytest.fixture
def sample_records():
    return [
        {
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-11-07"
        },
        {
            "title": "Bus",
            "amount": 40.0,
            "category": "Transport",
            "date": "2026-11-07"
        }
    ]


def test_export_and_import_json(tmp_path, sample_records):
    file_path = tmp_path / "expenses.json"

    export_records(sample_records, file_path)
    result = import_records(file_path)

    assert result == sample_records


def test_export_and_import_csv(tmp_path, sample_records):
    file_path = tmp_path / "expenses.csv"

    export_records(sample_records, file_path)
    result = import_records(file_path)

    assert len(result) == 2
    assert result[0]["title"] == "Lunch"
    assert float(result[0]["amount"]) == 250.0


def test_import_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        import_records(file_path)


def test_import_unsupported_format(tmp_path):
    file_path = tmp_path / "expenses.txt"
    file_path.write_text("test")

    with pytest.raises(ValueError):
        import_records(file_path)


def test_export_empty_csv(tmp_path):
    file_path = tmp_path / "empty.csv"

    with pytest.raises(ValueError):
        export_records([], file_path)


def test_import_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid json")

    with pytest.raises(json.JSONDecodeError):
        import_records(file_path)
