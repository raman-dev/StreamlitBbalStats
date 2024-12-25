import streamlit as st
import pandas as pd
import altair as alt




antibiotics = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/burtin.json'


st.header('Scales, Axes and Legends')
st.write(pd.read_json(antibiotics))

'''Data is clustered to the left '''
st.write(alt.Chart(antibiotics).mark_circle().encode(
    alt.X('Neomycin:Q')
))

'''
    
    Default is linear mapping between largest and smallest value\n
    Change the scale to logarithmic
'''
st.write(alt.Chart(antibiotics).mark_circle().encode(
    alt.X('Neomycin:Q',
          sort='descending',
          scale=alt.Scale(type='log'),
          title='Neomycin MIC (ug/ml, reverse log scale)')
))