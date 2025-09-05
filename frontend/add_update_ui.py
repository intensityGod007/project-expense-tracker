import datetime
import requests
import streamlit as st

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Date", value=datetime.date(2024, 8, 1), label_visibility="collapsed")
    response = requests.get(url=f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("Failed to fetch data")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expenses"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Rent"
                notes = ""

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, key=f"amount_{i}", value=amount,
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, key=f"category_{i}",
                                              index=categories.index(category), label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", key=f"notes_{i}", value=notes, label_visibility="collapsed")

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input,
            })

        submit_btn = st.form_submit_button()
        if submit_btn:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully")
            else:
                st.error("Failed to update expenses")