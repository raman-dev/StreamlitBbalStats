import streamlit as st
import pandas as pd
import altair as alt

from DataServer import DataServer

#st.cache_data decorator when returning serializable objects str,int float, DataFrames..etc
#st.cache_resource for non serializable objects
#will cache results 

server = DataServer()
playerList = server.get_players()
statsAvailable = server.get_stats_available()
#search box or list
#need a dropdown list of player selection
# def on_player_selectbox_change():
#     # st.write('You picked: ',st.session_state['selected_option'])
#     player_key = st.session_state['player_key']
#     drawChart(player_key,st.session_state['data_label'])

# def on_player_datalabel_change():
#     drawChart(st.session_state['player_key'],st.session_state['data_label'])

def slug_to_name(slug):
    return  slug.replace("-", " ").title()

@st.cache_data
def get_data_frame(player,stat):
    data = server.get_player_stat(name=player,stat=stat)
    result = data['docs'][0][stat]
    df = pd.DataFrame({
        'game':range(len(result)),
        stat:[int(x) for x in result]
    })
    return df


@st.cache_data
def get_data_frame_all_stats(player_key):
    raw_data = server.get_player_data(player_key)
    
    df = pd.DataFrame(raw_data['table'])
    return df.drop(df.columns[[2,3,4]],axis = 1)

def drawChart(df,player_key,data_label,upperMax):
    # st.altair_chart(line + dots)
    # st.write(df)
    # Create a line chart
    dimens = df.shape
    # st.write('Shaper => ',dimens)
    line = alt.Chart(df).mark_line().encode(
        x='game',
        y=data_label
    )

    # Create a dot (point) chart
    dots = alt.Chart(df).mark_point(size=100).encode(
        x='game',
        y=data_label
    )
    # st.line_chart(df,x='Game',y='points')
    # Calculate statistics
    mean_y = df[data_label].mean()
    median_y = df[data_label].median()
    # mad_y = df['points'].mad()

    # Create horizontal lines for mean ± MAD
    mean_line = alt.Chart(pd.DataFrame({data_label: [mean_y]})).mark_rule(color='cyan',strokeDash=[2,2]).encode(
        y=f'{data_label}:Q'
    )

    # Median line
    # median_line = alt.Chart(pd.DataFrame({data_label: [median_y]})).mark_rule(color='cyan', strokeDash=[2, 2]).encode(
    #     y=f'{data_label}:Q'
    # )

    upperRangeLine = alt.Chart(
        pd.DataFrame({
            'game':range(dimens[0]),
            'upper':[upperMax]*dimens[0]
        }),
    ).mark_line(color='rgb(255, 75, 75)').encode(x='game',y='upper')

    chart = (line + dots + mean_line +upperRangeLine)#
    st.title(slug_to_name(player_key))
    st.altair_chart(chart,use_container_width=True)
    return chart
    

# with st.form("single-stat-form"):
st.session_state['data_label'] = 'pts'

# stat_name_map = {
#     'pts':'points',
#     'trb':'Total Rebounds'
# }
# def stat_readable(stat):
#     if stat in stat_name_map:
#         return stat_name_map[stat].title()

@st.fragment
def chart_fragment():
    player_key = st.session_state['player_key']
    data_label = st.session_state['data_label']
    df_stat = get_data_frame(player_key,data_label)
    # df_all = get_data_frame_all_stats(player_key)
    lowerMax = 5
    upperMax = 35
    drawChart(df_stat,player_key,data_label,upperMax)
    # st.write(df_all)
    # upper = st.slider("upper",15,34)
    # lower = st.slider("lower",0,15)
    values = st.slider(
        "Range ",
        lowerMax,
        upperMax,
        (15,35),
        key='slider_vals',
        # on_change=st.rerun
    )
    # st.write("Values => ",values)

@st.fragment
def main_fragment():
    st.selectbox(
        "Player",
        playerList['players'],
        key='player_key',
        format_func= str.title,
    )

    #if a widget has a call back it is executed as a prefix to the entire page
    st.selectbox(
        "Stat",
        statsAvailable,
        key='data_label',
        format_func=str.title, 
    )
    #when the values change we need to render 2 lines in different locations
    chart_fragment()
main_fragment()

