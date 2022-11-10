import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from sql_metadata import parser

st.sidebar.markdown("Classic Models")
# PAGE THREE
st.title("Classic Models Data")

# Connection string
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rb@021114",
    database="classicmodels"
)

myCursor = myDB.cursor()

def displayTable():
    tableChoice = st.selectbox(
        "Select table to dislplay",
        ("Customers", "Employees", "Offices", "OrderDetails", "Orders", "Payments", "ProductLines", "Products")    
        )

    table = tableChoice.lower()
    myCursor.execute("SELECT * FROM " + table)
    # var1 = "SELECT * FROM " + table
    # columnNames = Parser(var1)
    # st.write(columnNames)

    df = pd.DataFrame(myCursor)

    if st.checkbox("Display table"):
        st.subheader(tableChoice)
        st.write(df)

def displayGraphs():
    # Products table and graph
    st.subheader("Products")
    myCursor.execute("SELECT productline, buyprice, MSRP FROM products GROUP BY productline")
    df = pd.DataFrame(myCursor, columns=["Product", "Buy Price", "MSRP"])
    if st.checkbox("Show table"):
        st.write(df)
    fig = px.bar(
        df,
        x="Product",
        y="Buy Price",
        title="Buy Price"
    )
    fig2 = px.bar(
        df,
        x="Product",
        y="MSRP",
        title="MSRP"
    )
    fig.show()
    fig2.show()

# Begin
displayTable()

if st.checkbox("View graphs"):
    displayGraphs()
# End