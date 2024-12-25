import streamlit as st
import pandas as pd
import altair as alt

# st.write('Hello World')

from vega_datasets import data

cars = data.cars()

chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin'
).interactive()

st.write(chart)

data = pd.DataFrame({
    'a':list('CCCDDDEEE'),
    'b':[2,7,4,1,2,6,8,4,7]
    })


chart = alt.Chart(data).mark_bar().encode(
    y='a',
    x='average(b)',
)
st.write(chart)