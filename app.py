import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

from DataServer import DataServer


#st.cache_data decorator when returning serializable objects str,int float, DataFrames..etc
#st.cache_resource for non serializable objects
#will cache results 

server = DataServer()
playerList = server.get_players()
statsAvailable = server.get_stats_available()
#search box or list

def slug_to_name(slug):
    return  slug.replace("-", " ").title()

@st.cache_data
def get_data_frame(player):
    data = server.get_player_data(player)
    n = len(data['date_game'])
    data['game'] = range(0,n) 
    df = pd.DataFrame(data)
    return df


# with st.form("single-stat-form"):
st.session_state['data_label'] = 'pts'
st.session_state['lowerMax'] = 15
st.session_state['upperMax'] = 35

def slider_on_change():
    newLowerMax,newUpperMax = st.session_state['slider_vals']
    st.session_state['lowerMax'] = newLowerMax
    st.session_state['upperMax'] = newUpperMax

@st.fragment
def main_fragment():
    
    player_select_column,range_select_column = st.columns(2)
    with player_select_column:
        st.selectbox(
                "Player",
                playerList['players'],
                key='player_key',
                format_func= slug_to_name,
            )

        #if a widget has a call back it is executed as a prefix to the entire page
        st.selectbox(
            "Stat",
            statsAvailable,
            key='data_label',
            format_func=str.title, 
        )
    df = get_data_frame(st.session_state['player_key'])

    stat_row = df[st.session_state['data_label']]
    min_stat,max_stat = stat_row.min(),stat_row.max()
    with range_select_column:
        #need a high low slider
        with st.form("stat-range"):
            low_high_range = st.select_slider('Low High Range',value=(min_stat,max_stat),options=list(range(min_stat,max_stat + 1)))
            
            render_extra = st.checkbox('Show',value=False)
            st.form_submit_button('Update chart')
        

    
    line = alt.Chart(df).mark_line().encode(
        alt.X('game:Q'),
        alt.Y(f'{st.session_state["data_label"]}:Q'),
    )

    #mark_rule for horizontal lines
    avg_line = alt.Chart(df).mark_rule(color='cyan',strokeDash=[2,2]).encode(
        y=f'mean({st.session_state["data_label"]}):Q'
    )
    num_games = len(df['game'])
    
    low_line  = alt.Chart(pd.DataFrame({'low':[low_high_range[0]] * num_games})).mark_rule(color='orangered').encode(y='low:Q')
    high_line = alt.Chart(pd.DataFrame({'high':[low_high_range[1]] * num_games})).mark_rule(color='limegreen').encode(y='high:Q')
    
    
    points = alt.Chart(df).mark_point(size=100).encode(
        alt.X('game'),
        alt.Y(f'{st.session_state["data_label"]}:Q')
    )

    st.header(slug_to_name(st.session_state['player_key']))
    result_chart = line + points + avg_line
    if render_extra:
        result_chart += low_line + high_line
    st.altair_chart(result_chart,use_container_width=True)

main_fragment()
