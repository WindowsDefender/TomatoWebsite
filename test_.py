#from keplergl import KeplerGl
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os
import geopy
import pickle
from geopy.geocoders import Nominatim
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title='PTAB DATA ACCESS', page_icon='🍅')
st.header('PTAB DATA ACCESS')
st.subheader("Tomato Project")
st.write("Acknowledgements: This work is supported by AFRI Competitive Grant no. 2020-67021-32855/project accession no. 1024262 from the USDA National Institute of Food and Agriculture. This grant is being administered through AIFS: the AI Institute for Next Generation Food Systems. https://aifs.ucdavis.edu. Tomato data are from the Processing Tomato Advisory Board public database: http://www.ptab.org.")
with open("dt_odj_cache.db", "rb") as infile:
  dt_obj = pickle.load(infile)
  infile.close()

df = None
with open ("dataframe.db", "rb") as infile:
  df = pickle.load(infile)
  infile.close()


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