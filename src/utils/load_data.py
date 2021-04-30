import pandas as pd
import streamlit as st

@st.cache
def load_data(DATA_URL):
    return pd.read_csv(DATA_URL)
