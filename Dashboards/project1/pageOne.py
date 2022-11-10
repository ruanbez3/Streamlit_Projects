from turtle import color
import streamlit as st
import pandas as pd
import mysql.connector

st.sidebar.markdown("Sales")
# PAGE ONE

# Connection string
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rb@021114",
    database="mydatabase"
)

myCursor = myDB.cursor()

myCursor.execute("SELECT * FROM sales")
df = pd.DataFrame(myCursor, columns=["Year", "Sales"])

# Begin
st.title("Sales per year database")

col1, col2 = st.columns([3, 7])

with col1:
    if st.button("View data in table"):
        with col2:
            st.write(df)

    if st.button("View bar chart"):
        with col2:
            st.bar_chart(
                df,
                x="Year",
                y="Sales",
                
            )

    if st.button("View line chart of data"):
        with col2:
            st.line_chart(
                df,
                x="Year",
                y="Sales"
        )

# End