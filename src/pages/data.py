import folium as folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from src.utils.load_data import load_data
from PIL import Image
from datetime import datetime

def main():
    img = Image.open('assets/logo.png')
    st.image(img)
    st.title('Data Snapshot')
    date = datetime.today()
    df = None
    load_state = st.text('Loading data.......')
    while True:
        try:
            df = load_data('src/data/data.csv')
        except Exception as e:
            print('File not found')
            continue
        break
    load_state.text('Loading data.......done!')

    # if st.checkbox('Member population distribution map', value=True):
    #     with st.beta_container():
    #         with st.spinner('Rendering chart...'):
    #             world_map = folium.Map(tiles="OpenStreetMap", zoom_start=105)
    #             marker_cluster = MarkerCluster().add_to(world_map)
    #             # for each coordinate, create circlemarker of user percent
    #             data = df[['Latitude', 'Longitude']].dropna()
    #             for i in range(len(data)):
    #                 lat = data.iloc[i]['Latitude']
    #                 long = data.iloc[i]['Longitude']
    #                 radius = 5
    #                 popup_text = """Country : {df.iloc[i]['Country']}<br>%of Users : {}<br>"""
    #                 # popup_text = popup_text.format(df.iloc[i]['Country'],
    #                 #                         df.iloc[i]['Gender']
    #                 #                         )
    #                 folium.CircleMarker(location=[lat, long], radius=radius, popup=popup_text, fill=True).add_to(marker_cluster)
    #
    #             # call to render Folium map in Streamlit
    #             folium_static(world_map)
    if st.checkbox('Show raw data', value=True):
        st.subheader('Raw data')
        st.write(df)
    st.subheader('Quick facts')
    st.markdown(f'* The Room has members in {len(df["Continent"].unique())} continents and {len(df["Country"].unique())} countries and {len(df["City"].unique())} cities around the world.')
    st.markdown(f'* There are {len(df["Customer Segment"].unique())} customer segments, {len(df["Membership Type"].unique())} membership types, and {len(df["Membership Level"].unique())} membership levels.')
    st.markdown(f'* Membership consists of {len(df[df["Gender"] == "male"])} males and {len(df[df["Gender"] == "female"])} females.')