import streamlit as st
import pandas as pd
import altair as alt


st.header('Multi-View Composition')

weather = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/weather.csv'

df = pd.read_csv(weather)
st.write(df.head(10))
st.write(df.tail(10))

'''
    2 different y axis on the same x
'''
st.write(
    alt.Chart(weather).mark_area().encode(
        alt.X('month(date):T'),
        alt.Y('average(temp_max):Q'),
        alt.Y2('average(temp_min):Q')
    )
)

st.write(alt.Chart(weather).mark_area(opacity=0.3).encode(
    alt.X('month(date):T'),
    alt.Y('average(temp_max):Q'),
    alt.Y2('average(temp_min):Q'),
    alt.Color('location:N')
))

'''
    showing midpoint between min and max daily temps
'''
st.write(alt.Chart(weather).mark_line().transform_calculate(
  temp_mid='(+datum.temp_min + +datum.temp_max) / 2'
).encode(
  alt.X('month(date):T'),
  alt.Y('average(temp_mid):Q'),
  alt.Color('location:N')
))