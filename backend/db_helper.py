import mysql.connector
from contextlib import contextmanager
from logger_setup import setup_logger


logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='expense_manager'
    )

    if connection.is_connected():
        print("Connection successful")
    else:
        print("Connection unsuccessful")

    # cursor = connection.cursor()    # return table in tuple format
    cursor = connection.cursor(dictionary=True)    # return table in dictionary format
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with date: {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
        "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
        (expense_date, amount, category, notes)
        )


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def fetch_expenses_summary(start_date, end_date):
    logger.info(f"fetch_expenses_summary called with start_date: {start_date}, end_date: {end_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
                        FROM expenses
                        WHERE expense_date BETWEEN %s and %s
                        GROUP BY category''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


if __name__ == '__main__':
    # insert_expense("2024-08-20", "300", "Food", "Panipuri")
    # delete_expenses_for_date("2024-08-20")
    expenses = fetch_expenses_for_date('2024-09-02')
    # expenses = fetch_expenses_summary("2024-08-01", "2024-08-05")
    for expense in expenses:
        print(expense)
