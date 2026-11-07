
import json
import pytest

import storage


def test_save_and_load_expenses(tmp_path, monkeypatch):
    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    expenses = [
        {
            "id": 1,
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-11-07"
        }
    ]

    storage.save_expenses(expenses)

    result = storage.load_expenses()

    assert result == expenses


def test_load_missing_file(tmp_path, monkeypatch):
    test_file = tmp_path / "missing.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    assert storage.load_expenses() == []


def test_load_empty_file(tmp_path, monkeypatch):
    test_file = tmp_path / "empty.json"
    test_file.write_text("")

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    assert storage.load_expenses() == []


def test_load_invalid_json(tmp_path, monkeypatch):
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json")

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    with pytest.raises(ValueError):
        storage.load_expenses()
