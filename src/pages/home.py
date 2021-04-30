import streamlit as st
from PIL import Image

def main():
    image = Image.open('assets/title.png')
    st.image(image)
    st.title('Data Analyst Recruitment Assignment')
    st.write('''
    This web-application will serve to analyze and visualize in accordance with the tasks laid out in the Data Analyst Recruitment Assignment.
    ''')
    st.markdown('## Tasks')
    st.markdown('You are tasked with creating visualizations to help inform the senior leadership team of the state of data about these users.\n'
                '* Your dashboard should include a visualization showing the gender distribution of the users;\n'
                '* Your dashboard should include a visualization showing the distribution of the users by location;\n'
                '* Create visualizations for any other attributes that you believe to be useful and add them to your dashboard;\n'
                '* Add to the dashboard a visualization that captures the overall completeness of the data.'
                )