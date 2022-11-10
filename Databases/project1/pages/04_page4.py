from asyncore import write
from json import detect_encoding
from operator import index
from textwrap import wrap
from tkinter import OFF
from turtle import width
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import plotly.express as px

# CONNECTION
connection_string = ('DRIVER={SQL Server};'
                    'SERVER=LAPTOP-ABPOUMCR\SQLEXPRESS;'
                    'DATABASE=FinTables')
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)
connection = engine.raw_connection()
myCursor = connection.cursor()

full_table = pd.read_sql("SELECT * FROM dbo.LoanApplications", engine)

# FUNCTIONS
def AcceptedCount():
    table = pd.read_sql("SELECT ClientRefId, AcceptedDate, AutoApproved, InstallmentAmount, Amount FROM dbo.LoanApplications", engine)
    # st.table(table)

    col1, col2 = st.columns(2)
    # get count from sql
    accepted = pd.read_sql("SELECT COUNT(*) AS [Approved] FROM dbo.LoanApplications WHERE AutoApproved = 1", engine)._get_value(0, "Approved")
    declined = pd.read_sql("SELECT COUNT(*) AS [Declined] FROM dbo.LoanApplications WHERE AutoApproved = 0", engine)._get_value(0, "Declined")
    accept_decline = pd.DataFrame([accepted, declined], index=["Approved", "Declined"])
   
    with col1:
        st.write("#### Loans approved")
        st.write(accepted)
        st.write("#### Loans declined")
        st.write(declined)

    with col2:
        fig = px.bar(
            accept_decline,
            title="Loan count"
        )
        fig.update_layout(width=500, height=300)
        st.write(fig)
    return

def LoanCounts():
    year_counts = pd.read_sql("SELECT * FROM dbo.LoanApplications WHERE ", engine)
    return
    
# BEGIN 
st.title("Loan Applications Table")

AcceptedCount()

# END