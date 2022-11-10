import time
from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Live Dashboard",
    page_icon="✅",
    layout="wide"
)

st.sidebar.markdown("DB 3")

dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

st.title("Real time science dashboard")

# filter from data
jobFilter = st.selectbox("Select the job", pd.unique(df["job"]))

df = df[df["job"] == jobFilter]

# st.markdown("### Detailed data")
# st.write(df)

# for seconds in range(200):
    
#     df["age_new"] = df["age"] * np.random.choice(range(1, 5))
#     df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))
#     time.sleep(1)

placeholder = st.empty()

with placeholder.container():
    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Age ⏳",
        value=round(10),
        delta=round(10) - 10,
    )
        
    col2.metric(
        label="Married Count 💍",
        value=int(10),
        delta=-10 + 10,
    )

    col3.metric(
        label="A/C Balance ＄",
        value=f"$ {round(10,2)} ",
        delta=-round(10/2) * 100,
    )

    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("### First chart")
        fig = px.density_heatmap(
            data_frame=df, y="age", x="marital"
        )
        st.write(fig)

    with fig_col2:
        st.markdown("### Second chart")
        fig2 = px.histogram(data_frame=df, x="age")
        st.write(fig2)