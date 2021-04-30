import streamlit as st
from PIL import Image


def main():
    with st.beta_container():
        st.subheader('Missing Values Analysis')
        img = Image.open('assets/missing.png')
        st.image(img)
