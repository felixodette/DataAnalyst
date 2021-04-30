import streamlit as st
import plotly.express as px
from src.utils.load_data import load_data

def main():
    df = load_data('src/data/data.csv')
    with st.beta_container():
        st.subheader('Gender Distribution')
        figure = px.sunburst(df, names=df['Gender'], parent=df['Membership Type'], value=df['Lifetime Days'].value_counts())
        st.plotly_chart(figure_or_data=figure)