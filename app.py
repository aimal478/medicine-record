import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if 'records' not in st.session_state:
    st.session_state.records = pd.DataFrame(columns=['Medicine', 'Type', 'Quantity', 'Date'])

st.title("💊 Medical Shop Manager")
st.subheader("📋 Record Medicine Sales and Purchases")

# Input form
with st.form("transaction_form"):
    medicine = st.text_input("Medicine Name")
    trans_type = st.selectbox("Transaction Type", ["Purchase", "Sale"])
    quantity = st.number_input("Quantity", min_value=1)
    date = st.date_input("Date", value=datetime.today())
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        new_entry = pd.DataFrame([[medicine, trans_type, quantity, date]],
                                 columns=['Medicine', 'Type', 'Quantity', 'Date'])
        st.session_state.records = pd.concat([st.session_state.records, new_entry], ignore_index=True)
        st.success("Transaction added!")

# Show records
st.subheader("📊 Transaction History")
st.dataframe(st.session_state.records)

# Stock Report
st.subheader("📦 Current Stock Report")
if not st.session_state.records.empty:
    purchases = st.session_state.records[st.session_state.records['Type'] == 'Purchase'].groupby('Medicine')['Quantity'].sum()
    sales = st.session_state.records[st.session_state.records['Type'] == 'Sale'].groupby('Medicine')['Quantity'].sum()
    stock = purchases.subtract(sales, fill_value=0).astype(int)
    stock_df = stock.reset_index()
    stock_df.columns = ['Medicine', 'Current Stock']
    st.dataframe(stock_df)
else:
    st.info("No records yet.")

# Optional: Download as CSV
st.download_button("📥 Download Transaction History", data=st.session_state.records.to_csv(index=False),
                   file_name="transaction_history.csv", mime="text/csv")
