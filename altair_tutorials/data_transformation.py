import streamlit as st
import pandas as pd
import altair as alt

from vega_datasets import data as vega_data


st.header('Data Transformation')
movies_url = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/movies.json'
movies = pd.read_json(movies_url)

st.write(movies.head(5))


st.subheader('Histograms')

st.write(alt.Chart(movies_url).mark_circle().encode(
    alt.X('Rotten_Tomatoes_Rating:Q',bin=True),#bins with a span increas max bins to reduce span
    alt.Y('IMDB_Rating:Q')
))


st.write(alt.Chart(movies_url).mark_circle().encode(
    alt.X('Rotten_Tomatoes_Rating:Q',bin=alt.BinParams(maxbins=20)),#
    alt.Y('IMDB_Rating:Q')
))

'''
    Count number of records in bins
'''
st.write(alt.Chart(movies_url).mark_circle().encode(
    alt.X('Rotten_Tomatoes_Rating:Q',bin=alt.BinParams(maxbins=20)),
    alt.Y('count()')
))

st.write(alt.Chart(movies_url).mark_bar().encode(
    alt.X('Rotten_Tomatoes_Rating:Q', bin=alt.BinParams(maxbins=20)),
    alt.Y('count()')
))

st.write(alt.Chart(movies_url).mark_bar().encode(
    alt.X('IMDB_Rating:Q',bin=alt.BinParams(maxbins=20)),
    alt.Y('count()')
))

st.subheader('Aggregation')
'''
    More aggregation possible using average,median,min or max refer to Altair documentation
'''

st.subheader('Filter')

st.write(alt.Chart(movies_url).mark_circle().encode(
    alt.X('Rotten_Tomatoes_Rating:Q'),
    alt.Y('IMDB_Rating:Q')
).transform_filter('datum.Major_Genre == "Romantic Comedy"'))

'''
    Use predicate test to filter data
    here year(datum.Release_Date) < 1970
'''
st.write(
    alt.Chart(movies_url).mark_circle().encode(
    alt.X('Rotten_Tomatoes_Rating:Q'),
    alt.Y('IMDB_Rating:Q')
    ).transform_filter('year(datum.Release_Date) < 1970')
)