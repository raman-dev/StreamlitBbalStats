import streamlit as st
import pandas as pd
import altair as alt

from DataServer import DataServer

#st.cache_data decorator when returning serializable objects str,int float, DataFrames..etc
#st.cache_resource for non serializable objects
#will cache results 

server = DataServer()
playerList = server.get_players()
#search box or list
#need a dropdown list of player selection
def on_player_selectbox_change():
    # st.write('You picked: ',st.session_state['selected_option'])
    player_key = st.session_state['player_key']
    showPlayerData(player_key,st.session_state['data_label'])

def on_player_datalabel_change():
    showPlayerData(st.session_state['player_key'],st.session_state['data_label'])

def slug_to_name(slug):
    return  slug.replace("-", " ").title()

@st.cache_data
def get_data_frame(player_key,data_label):
    data = None
    match data_label:
        case 'points':
            data = server.get_player_points(player_key)
        case 'rebounds':
            data = server.get_player_rebounds(player_key)
    # print(pointsData)
    df = pd.DataFrame({
        'game':range(len(data[data_label])),
        data_label:[int(x) for x in data[data_label]]
    })
    return df

def showPlayerData(player_key,data_label):
    # st.altair_chart(line + dots)
    # st.write(df)
    df = get_data_frame(player_key,data_label)
    # Create a line chart
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
    mean_line = alt.Chart(pd.DataFrame({data_label: [mean_y]})).mark_rule(color='red').encode(
        y=f'{data_label}:Q'
    )

    # Median line
    median_line = alt.Chart(pd.DataFrame({data_label: [median_y]})).mark_rule(color='cyan', strokeDash=[2, 2]).encode(
        y=f'{data_label}:Q'
    )

    # mad_lines = alt.Chart(pd.DataFrame({'points': [mean_y - mad_y, mean_y + mad_y]})).mark_rule(color='orange', strokeDash=[5, 5]).encode(
    #     y='points:Q'
    # )
    chart = (line + dots + mean_line + median_line)#
    st.title(slug_to_name(player_key))
    st.altair_chart(chart,use_container_width=True)

# def showPlayerData(player_key):
#     # st.altair_chart(line + dots)
#     # st.write(df)
#     df = get_data_frame(player_key)
#     # Create a line chart
#     line = alt.Chart(df).mark_line().encode(
#         x='game',
#         y='points'
#     )

#     # Create a dot (point) chart
#     dots = alt.Chart(df).mark_point(size=100).encode(
#         x='game',
#         y='points'
#     )
#     # st.line_chart(df,x='Game',y='points')
#     # Calculate statistics
#     mean_y = df['points'].mean()
#     median_y = df['points'].median()
#     # mad_y = df['points'].mad()

#     # Create horizontal lines for mean ± MAD
#     mean_line = alt.Chart(pd.DataFrame({'points': [mean_y]})).mark_rule(color='red').encode(
#         y='points:Q'
#     )

#     # Median line
#     median_line = alt.Chart(pd.DataFrame({'points': [median_y]})).mark_rule(color='cyan', strokeDash=[2, 2]).encode(
#         y='points:Q'
#     )

#     # mad_lines = alt.Chart(pd.DataFrame({'points': [mean_y - mad_y, mean_y + mad_y]})).mark_rule(color='orange', strokeDash=[5, 5]).encode(
#     #     y='points:Q'
#     # )
#     chart = (line + dots + mean_line + median_line)#
#     st.title(slug_to_name(player_key))
#     st.altair_chart(chart,use_container_width=True)
    

st.session_state['data_label'] = 'points'
player_selectbox = st.selectbox(
    "Player",
    playerList['players'],
    key='player_key',
    format_func= slug_to_name,
    on_change=on_player_selectbox_change
)

stat_selectbox = st.selectbox(
    "Stat",
    ['points','rebounds'],
    key='data_label',
    format_func=slug_to_name, 
    on_change=on_player_datalabel_change
)

st.write('You picked: ',player_selectbox)
showPlayerData(playerList['players'][0],'points')