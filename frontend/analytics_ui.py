import datetime
import requests
import streamlit as st
import pandas as pd
import numpy as np

API_URL = "http://localhost:8000"

def analytics_tab():
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", value=datetime.date(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", value=datetime.date(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        response = requests.post(f"{API_URL}/analytics", json=payload)
        if response.status_code != 200:
            st.error(response.text)

        response = response.json()

        data = {
            "Category": list(response.keys()),
            "Total": [response[category]['total'] for category in response],
            "Percentage": [response[category]['percentage'] for category in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values('Percentage', ascending=False)
        df_sorted["Total"] = df_sorted["Total"].map(lambda x: f"{x:.2f}")
        df_sorted["Percentage"] = df_sorted["Percentage"].map(lambda x: f"{x:.2f}")

        st.bar_chart(data=df.set_index('Category')["Percentage"], width=0, height=0)

        st.table(df_sorted.set_index("Category"))