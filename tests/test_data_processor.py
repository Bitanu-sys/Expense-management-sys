
import pytest

from data_processor import process_records


@pytest.fixture
def sample_records():
    return [
        {
            "title": " Lunch ",
            "amount": "250",
            "category": " food ",
            "date": "2026-11-07"
        },
        {
            "title": "",
            "amount": "invalid",
            "category": "Travel",
            "date": "2026-11-07"
        },
        {
            "title": "Lunch",
            "amount": "250",
            "category": "food",
            "date": "2026-11-07"
        }
    ]


def test_process_records_counts(sample_records):
    result = process_records(sample_records)

    assert result["valid_count"] == 1
    assert result["rejected_count"] == 2


def test_process_records_cleans_data(sample_records):
    result = process_records(sample_records)

    expense = result["valid_records"][0]

    assert expense["title"] == "Lunch"
    assert expense["category"] == "food"
    assert expense["amount"] == 250.0


def test_process_records_rejects_invalid_data(sample_records):
    result = process_records(sample_records)

    assert "Title cannot be empty." in (
        result["rejected_records"][0]["reason"]
    )


def test_process_records_detects_duplicates(sample_records):
    result = process_records(sample_records)

    assert result["rejected_records"][1]["reason"] == (
        "Duplicate record"
    )


def test_process_empty_records():
    result = process_records([])

    assert result["valid_records"] == []
    assert result["rejected_records"] == []
    assert result["valid_count"] == 0
    assert result["rejected_count"] == 0
