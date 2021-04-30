import os
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from src.utils.load_data import load_data
import pandas as pd
import math
from folium.plugins import MarkerCluster
import folium
from streamlit_folium import folium_static


@st.cache
def plot_snapshot_numbers(df, colors, country=None):
    with st.spinner('Rendering chart...'):
        colors = px.colors.qualitative.D3
        if country:
            df = df[df['Country'] == country]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            df[['Gender', 'Membership Level']].columns.tolist(),
            df[['Gender', 'Membership Level']].values(),
            text=df[['Gender', 'Membership Level']].count().values(),
            orientation='h',
        ))


def cat_numbers(df, col):
    new_data = pd.DataFrame(df[col].value_counts())
    new_data.reset_index(inplace=True)
    new_data = new_data.rename(columns={'index': col, col: 'Number'})
    new_data = new_data.dropna(axis=1)
    return new_data


def pie_chart(df, name, title):
    with st.spinner('Rendering chart...'):
        figure = px.pie(df, values='Number', names=name, title=title)
        st.plotly_chart(figure_or_data=figure)


def exp_data(country, data):
    expander = st.beta_expander(f'{country} Analysis')
    expander.write(
        f'{country} has {round((data.loc[0]["Number"] / (data.loc[0]["Number"] + data.loc[1]["Number"])) * 100, 1)}% {data.loc[0]["Gender"]} and {round((data.loc[1]["Number"] / (data.loc[0]["Number"] + data.loc[1]["Number"])) * 100, 1)}% {data.loc[1]["Gender"]} membership.')


def main():
    pio.templates.default = 'plotly_dark'
    df = None
    while True:
        try:
            df = load_data('src/data/data.csv')
        except Exception as e:
            print('File not found')
            continue
        break
    granularity = st.sidebar.selectbox("Granularity", ["Worldwide", "Continent", "Country"])
    if granularity == "Worldwide":
        viz = ['Global Member Distribution', 'Gender Distribution', 'Membership Type', 'Membership Level']
        choice = st.sidebar.selectbox('Choose Visualization', viz)
        st.title("Member Distribution")
        if choice == 'Global Member Distribution':
            conti = pd.DataFrame(df.groupby('Continent')['Gender'].value_counts()).rename(columns={'Gender': 'Numbers'})
            conti = conti.unstack(level=0)
            conti.columns = conti.columns.droplevel([0])
            conti = conti.rename_axis([None], axis=1).reset_index()
            with st.beta_container():
                with st.spinner('Rendering chart...'):
                    world_map = folium.Map(tiles="OpenStreetMap", zoom_start=2000)
                    marker_cluster = MarkerCluster().add_to(world_map)
                    data = df[['Latitude', 'Longitude', 'Country', 'Gender']].dropna()
                    for i in range(len(data)):
                        lat = data.iloc[i]['Latitude']
                        long = data.iloc[i]['Longitude']
                        radius = 5
                        # popup_text = f"Country : {data.iloc[i]['Country']}<br>%of Users : {}<br>"
                        # popup_text = popup_text.format(data.iloc[i]['Country'], data.iloc[i]['Gender'])
                        folium.CircleMarker(location=[lat, long], radius=radius, fill=True).add_to(
                            marker_cluster)

                    # call to render Folium map in Streamlit
                    folium_static(world_map)
                if st.checkbox('Show raw data'):
                    st.write(conti)
                expander = st.beta_expander('Analysis')
                expander.write(f'Africa has the highest membership rate at {round(((669+708)/1707)*100, 2)}%, followed by North America {round(((71+95)/1707)*100, 2)}%, Europe {round(((669+708)/1707)*100, 2)}%, Asia {round((20/1707)*100, 2)}% and finally Oceania {round((2/1707)*100, 2)}%')
        elif choice == 'Gender Distribution':
            with st.beta_container():
                st.subheader('Worldwide Member Gender Distribution')
                data = cat_numbers(df, 'Gender')
                pie_chart(data, 'Gender', 'Global Member Gender Distribution')
                expander = st.beta_expander('Analysis')
                expander.write(f"The Room's membership consists of 52.1% males and 47.9% females.")
        elif choice == 'Membership Type':
            mem = pd.DataFrame(df.groupby('Gender')['Membership Type'].value_counts()).rename(
                columns={'Membership Type': 'Number'})
            mem = mem.unstack(level=1)
            mem.columns = mem.columns.droplevel([0])
            mem = mem.rename_axis([None], axis=1).reset_index()
            mem.drop(columns='NONE')
            with st.beta_container():
                fig = px.bar(mem, x='Gender', y=['Founding Member', 'Free Trial', 'Premium Paying', 'Staff Membership'])
                fig.update_layout(barmode='group')
                st.plotly_chart(figure_or_data=fig)
                expander = st.beta_expander('Analysis')
                expander.write(f'A majority, 55.5%, of members hold Free Trial accounts (53.4% female and 57.3%). '
                               f'11.6% on the Premium Paying Plan, 20.3% are Founding Members and 12.1% are on Staff '
                               f'Membership.')
        elif choice == 'Membership Level':
            mlevel = pd.DataFrame(df.groupby('Membership Level')['Gender'].value_counts()).rename(
                columns={'Membership Level': 'Number'})
            mlevel = mlevel.unstack(level=1)
            mlevel.columns = mlevel.columns.droplevel([0])
            mlevel = mlevel.rename_axis([None], axis=1).reset_index()
            mlevel['male%'] = round(mlevel['male'] / (mlevel['male'] + mlevel['female']) * 100, 2)
            mlevel['female%'] = round(mlevel['female'] / (mlevel['male'] + mlevel['female']) * 100, 2)
            with st.beta_container():
                fig = px.bar(mlevel, x='Membership Level', y=['female%', 'male%'])
                fig.update_layout(title_text="Membership Level Distribution", barmode="stack",
                                  uniformtext=dict(mode="hide", minsize=10), )
                st.plotly_chart(figure_or_data=fig)
                expander = st.beta_expander('Analysis')
                expander.write(f'A majority of the members, {round(363/(363+242+200),2)*100}% are Mid-career Leaders. '
                               f'However, gender distribution across the membership levels is relatively even, '
                               f'males being dominating membership with little margin:\n '
                               '* Young Leader: 50.98% male and 49.02% female'
                               '* Mid-career Leader: 51.21% male and 48.79% female'
                               '* Senior Leader: 53.99% male and 49.02% female')
    if granularity == "Country":
        country = st.sidebar.selectbox('country', df['Country'].unique())
        st.title(country)
        graph_type = st.selectbox("Choose visualization",
                                  ['Gender', 'Membership Type Distribution', 'Membership Level Distribution'])
        if graph_type == "Gender":
            st.subheader("Gender Distribution")
            with st.beta_container():
                data = cat_numbers(df[df['Country'] == country], 'Gender')
                st.write(data)
                pie_chart(data, 'Gender', 'Gender Distribution')
                expander = st.beta_expander(f'{country} Analysis')
                expander.write(f'{country} has {round((data.loc[0]["Number"] / (data.loc[0]["Number"] + data.loc[1]["Number"]))*100,1)}% {data.loc[0]["Gender"]} and {round((data.loc[1]["Number"] / (data.loc[0]["Number"] + data.loc[1]["Number"]))*100,1)}% {data.loc[1]["Gender"]} membership.')
                # exp_data(f'{country}', data)
        elif graph_type == "Membership Type Distribution":
            st.subheader("Membership Type Distribution")
            with st.beta_container():
                data = cat_numbers(df[df['Country'] == country], 'Membership Type')
                pie_chart(data, 'Membership Type', 'Membership Type Distribution')
        elif graph_type == "Membership Level Distribution":
            st.subheader("Membership Level Distribution")
            with st.beta_container():
                data = cat_numbers(df[df['Country'] == country], 'Membership Level')
                pie_chart(data, 'Membership Level', 'Membership Level Distribution')
    elif granularity == "Continent":
        continent = st.sidebar.selectbox('continent', df['Continent'].dropna().unique())
        st.title(continent)
        graph_type = st.selectbox("Choose visualization",
                                  ['Gender', 'Membership Type Distribution', 'Membership Level Distribution'])
        if graph_type == "Gender":
            st.subheader("Gender Distribution")
            with st.beta_container():
                data = cat_numbers(df[df['Continent'] == continent], 'Gender')
                pie_chart(data, 'Gender', 'Gender Distribution')
        elif graph_type == "Membership Type Distribution":
            with st.beta_container():
                data = cat_numbers(df[df['Continent'] == continent], 'Membership Type')
                pie_chart(data, 'Membership Type', 'Membership Type Distribution')
        elif graph_type == "Membership Level Distribution":
            with st.beta_container():
                data = cat_numbers(df[df['Continent'] == continent], 'Membership Level')
                pie_chart(data, 'Membership Level', 'Membership Level Distribution')
