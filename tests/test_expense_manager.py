import pytest

from expense_manager import (
    add_expense,
    search_expenses,
    delete_expense,
    calculate_summary
)


@pytest.fixture
def expenses():
    return [
        {
            "id": 1,
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-11-07"
        },
        {
            "id": 2,
            "title": "Bus Ticket",
            "amount": 40.0,
            "category": "Transport",
            "date": "2026-11-07"
        }
    ]


def test_add_expense(expenses):
    result = add_expense(
        expenses, "Coffee", 100, "Food", "2026-11-07"
    )

    assert result["id"] == 3
    assert result["title"] == "Coffee"
    assert len(expenses) == 3


def test_add_expense_with_invalid_amount(expenses):
    with pytest.raises(ValueError):
        add_expense(
            expenses, "Coffee", -100, "Food", "2026-11-07"
        )


def test_add_expense_with_empty_title(expenses):
    with pytest.raises(ValueError):
        add_expense(
            expenses, " ", 100, "Food", "2026-11-07"
        )


def test_search_expenses(expenses):
    results = search_expenses(expenses, "food")

    assert len(results) == 1
    assert results[0]["title"] == "Lunch"


def test_delete_expense(expenses):
    deleted = delete_expense(expenses, 1)

    assert deleted["title"] == "Lunch"
    assert len(expenses) == 1


def test_delete_invalid_id(expenses):
    with pytest.raises(ValueError):
        delete_expense(expenses, 99)


def test_calculate_summary(expenses):
    summary = calculate_summary(expenses)

    assert summary["total"] == 290.0
    assert summary["count"] == 2
    assert summary["categories"]["Food"] == 250.0
    assert summary["categories"]["Transport"] == 40.0


def test_empty_summary():
    summary = calculate_summary([])

    assert summary["total"] == 0
    assert summary["count"] == 0
    assert summary["categories"] == {}