from keplergl import KeplerGl
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
import geopy
from geopy.geocoders import Nominatim
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title='PTAB DATA ACCESS')
st.header('PTAB DATA ACCESS')
st.subheader("Developed with AIFS and PTAB")
st.write("Acknowledgements: This work is supported by AFRI Competitive Grant no. 2020-67021-32855/project accession no. 1024262 from the USDA National Institute of Food and Agriculture. This grant is being administered through AIFS: the AI Institute for Next Generation Food Systems. https://aifs.ucdavis.edu. Tomato data are from the Processing Tomato Advisory Board public database: http://www.ptab.org.")


geolocator = Nominatim(user_agent="Processing Plants")

import datetime as dt
import sqlite3
HEADER = ["Rejection Rate",
          "Date",
          "County",
          '#loads',
          "Tomato variety number",
          "Tomato variety name",
          "Usage from agseeds",
          "Tomato variety name agseeds",
          "Average worm/insect damage",
          "Average mold",
          "Average green",
          "Average material other than tomatoes",
          "Average color",
          "Average solids",
          "Average pH",
          "Day 0 high",
          'Day 0 low',
          "Day 1 high",
          'Day 1 low',
          "Day 2 high",
          'Day 2 low',
          "Day 3 high",
          'Day 3 low',
          "Day 4 high",
          'Day 4 low',
          "Day 5 high",
          'Day 5 low',
          "Day 6 high" , 
          'Day 6 low']

db_connector = sqlite3.connect("ptab_filtered_dataset.db")
data = db_connector.cursor().execute('SELECT "Rejection Rate", "Date", "County", "#loads", "Tomato variety number", "Tomato variety name", "Usage from agseeds", "Tomato variety name agseeds", "Average worm/insect damage", "Average mold", "Average green", "Average material other than tomatoes", "Average color", "Average solids", "Average pH", "Day 0 high", "Day 0 low", "Day 1 high", "Day 1 low", "Day 2 high", "Day 2 low", "Day 3 high", "Day 3 low", "Day 4 high", "Day 4 low", "Day 5 high", "Day 5 low", "Day 6 high" , "Day 6 low" FROM ptab ORDER BY "date" DESC')
db_connector.commit()
data = data.fetchall()
unique_counties = db_connector.cursor().execute('SELECT DISTINCT County FROM ptab')
db_connector.commit()
unique_counties = unique_counties.fetchall()
cities_dict = dict()
for aCounty in unique_counties:
    addr = geolocator.geocode(aCounty[0])
    cities_dict[aCounty[0]] = (addr.longitude, addr.latitude)
city = []
lat = []
longitude = []
datetime = []
loads = []
rr = []
avg_green = []
avg_mold = []
avg_mot = []
avg_color = []
avg_solids = []
avg_ph = []
day_0_high = []
day_0_low = []
day_1_high = []
day_1_low = []
day_2_high = []
day_2_low = []
day_3_high = []
day_3_low = []
day_4_high = []
day_4_low = []
day_5_high = []
day_5_low = []
day_6_low = []
day_6_high = []
dt_obj = []
for each in data:
    if '' in each:
        continue
    city.append(each[HEADER.index("County")])
    lat.append(float(cities_dict[each[HEADER.index("County")]][1]))
    longitude.append(float(cities_dict[each[HEADER.index("County")]][0]))
    dstr = each[HEADER.index("Date")].split("-")
    dtr = dt.datetime(int(dstr[2]), int(dstr[0]), int(dstr[1])).strftime("%m/%d/%Y")
    datetime.append(dtr)
    dt_obj.append(dt.datetime(int(dstr[2]), int(dstr[0]), int(dstr[1])))
    loads.append(float(each[HEADER.index("#loads")]))
    rr.append(float(each[HEADER.index("Rejection Rate")]))
    avg_green.append(float(each[HEADER.index("Rejection Rate")]))
    avg_mold.append(float(each[HEADER.index("Average mold")]))
    avg_mot.append(float(each[HEADER.index("Average mold")]))
    avg_color.append(float(each[HEADER.index("Average color")]))
    avg_solids.append(float(each[HEADER.index("Average solids")]))
    avg_ph.append(float(each[HEADER.index("Average pH")]))
    day_0_high.append(float(each[HEADER.index("Day 0 high")]))
    day_0_low.append(float(each[HEADER.index("Day 0 low")]))
    day_1_high.append(float(each[HEADER.index("Day 1 high")]))
    day_1_low.append(float(each[HEADER.index("Day 1 low")]))
    day_2_high.append(float(each[HEADER.index("Day 2 high")]))
    day_2_low.append(float(each[HEADER.index("Day 2 low")]))
    day_3_high.append(float(each[HEADER.index("Day 3 high")]))
    day_3_low.append(float(each[HEADER.index("Day 3 low")]))
    day_4_high.append(float(each[HEADER.index("Day 4 high")]))
    day_4_low.append(float(each[HEADER.index("Day 4 low")]))
    day_5_high.append(float(each[HEADER.index("Day 5 high")]))
    day_5_low.append(float(each[HEADER.index("Day 5 low")]))
    day_6_high.append(float(each[HEADER.index("Day 6 high")]))
    day_6_low.append(float(each[HEADER.index("Day 6 low")]))
df = pd.DataFrame(
    {
        'County': city,
        'Latitude': lat,
        'Longitude': longitude,
        'loads' : loads,
        'Rejection Rate': rr,
        'avg_green' : avg_green,
        'avg_mold' : avg_mold,
        'avg_mot' : avg_mot,
        'avg_color' : avg_color,
        'avg_solids' : avg_solids,
        'avg_ph' : avg_ph,
        'day_0h' : day_0_high,
        'day_0l' : day_0_low,
        'day_1h' : day_1_high,
        'day_1l' : day_1_low,
        'day_2h' : day_2_high,
        'day_2l' : day_2_low,
        'day_3h' : day_3_high,
        'day_3l' : day_3_low,
        'day_4h' : day_4_high,
        'day_4l' : day_4_low,
        'day_5h' : day_5_high,
        'day_5l' : day_5_low,
        'day_6h' : day_6_high,
        'day_6l' : day_6_low,
        'datetime' : datetime
    }
    )
df['datetime'] = pd.to_datetime(df['datetime'])

County = df['County'].unique().tolist()
dtdf = df['datetime'].unique().tolist()
date_selection = st.slider('Date',
                           min_value=min(dt_obj),
                           max_value=max(dt_obj),
                           value=(min(dt_obj),max(dt_obj))
                           )

cs = st.multiselect('County',
                    County,
                    default=County)

mask = (df['County'].isin(cs)) & (df['datetime'].between(*date_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Number of available data after filtering: {number_of_result}*')
df = df[mask]
df.sort_values(by=['datetime'],ascending=True)
df = df.reset_index()
st.dataframe(df)
st.plotly_chart(
    px.pie(
        df,
        title='Number of total loads by counties',
        values='loads',
        names='County')
    )
st.line_chart(data=df['Rejection Rate'])