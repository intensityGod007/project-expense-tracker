from fastapi import FastAPI
from datetime import date
import db_helper
from pydantic import BaseModel
from typing import List
app = FastAPI()


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    return expenses


@app.post("/expenses/{expense_date}")
def add_expenses(expense_date: date, expenses: List[Expense]):
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}