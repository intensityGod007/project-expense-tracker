from backend import db_helper


def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date('2024-08-15')
    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10
    assert expenses[0]['category'] == "Shopping"


def test_fetch_expenses_for_invalid_date():
    expenses = db_helper.fetch_expenses_for_date('2024-08-20')
    assert len(expenses) == 0


def test_fetch_expenses_summary():
    summary = db_helper.fetch_expenses_summary("2099-01-01", "3000-01-01")
    assert len(summary) == 0