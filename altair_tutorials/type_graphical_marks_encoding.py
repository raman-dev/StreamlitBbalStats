import streamlit as st
import pandas as pd
import altair as alt

from vega_datasets import data as vega_data

data = vega_data.gapminder()

data.shape

st.table(data.head(5))

data2000 = data.loc[data['year'] == 2000]
st.table(data2000.head(5))

"""
Data types supported by Altair\n
    Nominal - Named data, comparisons supported are A = B or A != B
    Ordinal - Data with specific ordering, comparisions A < B or A > B
    Quantitative(Q) - Data with measurable numerical differences, subtypes interval,ratio
    Temporal(T) - Special case of quantitative values,namely timestamps

    2.2.5. Summary 
    "These data types are not mutually exclusive, but rather form a hierarchy: ordinal data support nominal (equality) comparisons, while quantitative data support ordinal (rank-order) comparisons.
     Moreover, these data types do not provide a fixed categorization.
     Just because a data field is represented using a number doesn’t mean we have to treat it as a quantitative type! 
     For example, we might interpret a set of ages (10 years old, 20 years old, etc) as nominal (underage or overage), ordinal (grouped by year), or quantitative (calculate average age)."
    
     Ref - https://idl.uw.edu/visualization-curriculum/altair_marks_encoding.html


"""

st.write(alt.Chart(data2000).mark_point().encode(
    alt.X('fertility:Q'),
    alt.Y('life_expect:Q')
))

st.write(alt.Chart(data2000).mark_point().encode(
    alt.X('fertility:Q', scale=alt.Scale(zero=False)),
    alt.Y('life_expect:Q', scale=alt.Scale(zero=False))
))

c = alt.Chart(data2000).mark_point(filled=True).encode(
    alt.X('fertility:Q'),
    alt.Y('life_expect:Q'),
    alt.Size('pop:Q', scale=alt.Scale(range=[0,1000])),
    alt.Color('cluster:N')
)

st.write(c)

st.write(alt.Chart(data2000).mark_point(filled=True).encode(
    alt.X('fertility:Q'),
    alt.Y('life_expect:Q'),
    alt.Size('pop:Q', scale=alt.Scale(range=[0,1000])),
    alt.Color('cluster:N'),
    alt.OpacityValue(0.5)
))