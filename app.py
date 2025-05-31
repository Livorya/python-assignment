import pandas as pd
import requests
from io import StringIO
import streamlit as st

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Livorya/python-assignment/refs/heads/main/data/diamonds.csv?token=GHSAT0AAAAAADEGUNIDTVQUU2CPFXKZGST62B24R2A"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None
    

st.write("# Diamonds!!")

df = load_data()
st.write("###### Table of Diamonds.csv")
st.dataframe(df)

