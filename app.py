import numpy as np
import pandas as pd

import math
import os
import sys

import streamlit as st
from streamlit_folium import folium_static
import folium

import matplotlib as mpl
import matplotlib.patheffects as effects
import matplotlib.pyplot as plt
import mplstereonet
import plotly.express as px
import plotly.io as pio
from scipy.optimize import basinhopping, least_squares, minimize
from io import StringIO


def make_map(pjcode, hole_no, test_location):
    
    for tiletype in ["OpenStreetmap", "Stamen Terrain", "Stamen Toner"]:
        m = folium.Map(
            location=test_location,
            tiles=tiletype,
            zoom_start=13,
            width=1200,
            height=800,
        )
        folium.Marker(test_location, popup="<i>" + hole_no + "<i>").add_to(m)
        m.save(f"{pjcode}_{hole_no}_map_{tiletype}.html")

    basemap_google = {
        "Google Maps": folium.TileLayer(
            tiles="http://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Maps",
            overlay=True,
            control=True,
        )
    }
    basemap_google["Google Maps"].add_to(m)
    m.save(f"{pjcode}_{hole_no}_map_GoogleMaps.html")
    minimize


def parse_dat(data):
    
    pjcode = data[0].strip() 
    hole_no = data[1].strip()
    test_location = [float(data[2].split(",")[0]), float(data[2].split(",")[1])]
    make_map(pjcode, hole_no, test_location)
    
    density, tdepth, tburden = [float(xx) for xx in data[3].replace("\n", "").split("\t")[0:3]]   
    x0 = [float(xx) for xx in data[4].replace("\n", "").split("\t")]
    
    norows = int(data[5].replace("\n", "").split("\t")[0])
    
    temp = list()
    for ii in range(0, norows, 1):
        temp.append(data[ii+6].replace("\n", "").split("\t"))

    m = pd.DataFrame(
        temp,
        columns=[
            "findex",
            "bbering",
            "binclin",
            "mdepth",
            "psm",
            "fstrike",
            "fdip",
            "dummy",
        ],
    )


if __name__ == "__main__":
    st.title('HF3D | 수압파쇄코드(test)')
    st.write('### 입력자료파일 선택')

    datfile = st.file_uploader("Choose a dat file")
    if datfile is not None:
        stringio = StringIO(datfile.getvalue().decode("utf-8"))
        string_data = stringio.readlines()
        parse_dat(string_data)

	
# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data
# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache)")
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)