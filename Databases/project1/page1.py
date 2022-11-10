from collections import _OrderedDictKeysView
from turtle import title
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

st.set_page_config(
    page_title="Customers",
    page_icon="✅",
    layout="wide"
)

st.title("Customers database")

# CONNECTION
connection_string = ('DRIVER={SQL Server};'
                    'SERVER=LAPTOP-ABPOUMCR\SQLEXPRESS;'
                    'DATABASE=mydatabase')
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.sidebar.markdown("DB 1")

# Tables
agents = pd.read_sql("SELECT * FROM AGENTS", engine, index_col="AGENT_CODE")
customers = pd.read_sql("SELECT * FROM CUSTOMER", engine, index_col="AGENT_CODE")
orders = pd.read_sql("SELECT * FROM ORDERS", engine, index_col="AGENT_CODE")
customer_data = pd.read_sql("SELECT DISTINCT CUST_COUNTRY, MAX(PAYMENT_AMT) AS PAYMENT, MAX(OUTSTANDING_AMT) AS OUTSTANDING FROM CUSTOMER GROUP BY CUST_COUNTRY", engine)

if st.checkbox("Agents"):
    st.write(agents)

if st.checkbox("Customers"):
    st.write(customers)

if st.checkbox("Orders"):
    st.write(orders)

st.subheader("Data to display")
st.markdown("#### Customers")
st.write(customer_data)

customer_graph = customer_data.pivot(
                                    index=["CUST_COUNTRY"], 
                                    columns=["PAYMENT", "OUTSTANDING"],
                                    values=["PAYMENT", "OUTSTANDING"],
                                    )

st.bar_chart(customer_graph)
