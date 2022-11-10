import csv
from tokenize import group
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import plotly.express as px

st.set_page_config(
    page_title="HR",
    page_icon="✅",
    layout="wide"
)

st.title("HR Database")

# CONNECTION
connection_string = ('DRIVER={SQL Server};'
                    'SERVER=LAPTOP-ABPOUMCR\SQLEXPRESS;'
                    'DATABASE=mydatabase2')
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.sidebar.markdown("HR Database")

# Tables
jobs = pd.read_sql("SELECT * FROM jobs", engine)
employees = pd.read_sql("SELECT * FROM employees", engine)
dependents = pd.read_sql("SELECT * FROM dependents", engine)
departments = pd.read_sql("SELECT * FROM departments", engine)
regions = pd.read_sql("SELECT * FROM regions", engine)
countries = pd.read_sql("SELECT * FROM countries", engine)
locations = pd.read_sql("SELECT * FROM locations", engine)

# Display tables
if st.sidebar.checkbox("Show Tables"):
    st.subheader("Jobs")
    st.write(jobs)
    st.subheader("Employees")
    st.write(employees)
    st.subheader("Dependents")
    st.write(dependents)
    st.subheader("Departments")
    st.write(departments)
    st.subheader("Regions")
    st.write(regions)
    st.subheader("Countries")
    st.write(countries)
    st.subheader("Locations")
    st.write(locations)

jobs_data = pd.read_sql("SELECT job_title, min_salary, max_salary FROM jobs", engine)
job_bar = jobs_data.pivot(index=["job_title"], columns=["min_salary", "max_salary"], values=["min_salary", "max_salary"])

st.write(jobs_data)

# Stacked bar chart
st.markdown("#### Plotly Express bar")
fig = px.bar(
    jobs_data,
    title="Minimum salary against Maximum",
    x="job_title",
    y=["min_salary", "max_salary"],
    barmode="group"
)
st.write(fig)

st.markdown("#### Streamlit bar_chart")
st.bar_chart(job_bar, use_container_width=True)

# Download file
downloadFile = jobs_data.to_parquet()

with st.sidebar:
    st.download_button(
        "Download",
        downloadFile,
        "jobsdata.gzip",
        key="download-csv"
    )

# Upload file from machine
uploadedFile = st.file_uploader("Choose a file")

if st.button("Show file"):
    file = pd.read_parquet(uploadedFile)
    st.write(file)