from audioop import add
from re import sub
import streamlit as st
import pandas as pd
import mysql.connector

st.sidebar.markdown("Users")
# PAGE TWO

# Connection string
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rb@021114",
    database="mydatabase"
)

myCursor = myDB.cursor()

# Begin
st.title("Users database")
    
myCursor.execute("SELECT * FROM users")
df = pd.DataFrame(myCursor, columns=["ID", "Name", "Surname", "Email"])
st.write(df)

# Clear table
if st.button("Clear table"):
    myCursor.execute("DELETE FROM users WHERE id > 0")
    myDB.commit()

col1, col2 = st.columns([5, 5])

with col1:
    if st.checkbox("Add User"):
        with col2:
            addForm = st.form(key="Add User", clear_on_submit=True)
            name = addForm.text_input("Name")
            surname = addForm.text_input("Surnmame")
            email = addForm.text_input("Email")
            submit = addForm.form_submit_button("Add")
            if submit:
                sql = "INSERT INTO users (name, surname, email) VALUES ('" + name + "', '"  + surname + "', '" + email + "')"
                myCursor.execute(sql)
                myDB.commit()            

    if st.checkbox("Sort"):
        with col2:
            sortForm = st.form("Sort", clear_on_submit=True)
            sortBy = sortForm.selectbox("Sort By", ("Ascending", "Descending"))
            submit = sortForm.form_submit_button("Done")
            if submit:
                if sortBy == "Ascending":
                    sql = "SELECT * FROM users ORDER BY id ASC"
                elif sortBy == "Descending":
                    sql = "SELECT * FROM users ORDER BY id DESC"
                myCursor.execute(sql)

    st.checkbox("Delete user")

# End