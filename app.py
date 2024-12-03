import streamlit as st
import pandas as pd
import requests
import altair as alt

#st.cache_data decorator when returning serializable objects str,int float, DataFrames..etc
#st.cache_resource for non serializable objects
#will cache results 
class DataServer:
    PLAYER_URL='http://localhost:5984/players'
    ALL_PLAYERS_VIEW = '/_design/allPlayers/_view/all-players-view'
    POINTS_VIEW = '/_design/allPlayers/_view/points-view'
    def get_players(self):
        #use requests library to request from the data server
        response = requests.get(DataServer.PLAYER_URL + DataServer.ALL_PLAYERS_VIEW)
        data = response.json()
        players = [x['key'] for x in data['rows']]
        return {'players':players,'count': data['total_rows']}
    
    def get_player_data(self,player):
        response = requests.get(DataServer.PLAYER_URL + f'/{player}')
        return response.json()
    
    def get_player_points(self,player):
        url = DataServer.PLAYER_URL +DataServer.POINTS_VIEW+ f'/?key="{player}"'
        print(url)
        response = requests.get(url)
        raw_data = response.json()
        return raw_data['rows'][0]['value']

server = DataServer()
playerList = server.get_players()
#search box or list
#need a dropdown list of player selection
def on_player_selectbox_change():
    # st.write('You picked: ',st.session_state['selected_option'])
    player_key = st.session_state['selected_option']
    showPlayerData(player_key)

def slug_to_name(slug):
    return  slug.replace("-", " ").title()

@st.cache_data
def get_data_frame(player_key):
    # data = server.get_player_data(player_key)
    pointsData = server.get_player_points(player_key)
    # print(pointsData)
    df = pd.DataFrame({
        'game':range(len(pointsData['points'])),
        'points':[int(x) for x in pointsData['points']]
    })
    return df

def showPlayerData(player_key):
    # st.altair_chart(line + dots)
    # st.write(df)
    df = get_data_frame(player_key)
    # Create a line chart
    line = alt.Chart(df).mark_line().encode(
        x='game',
        y='points'
    )

    # Create a dot (point) chart
    dots = alt.Chart(df).mark_point(size=100).encode(
        x='game',
        y='points'
    )
    # st.line_chart(df,x='Game',y='points')
    # Calculate statistics
    mean_y = df['points'].mean()
    median_y = df['points'].median()
    # mad_y = df['points'].mad()

    # Create horizontal lines for mean ± MAD
    mean_line = alt.Chart(pd.DataFrame({'points': [mean_y]})).mark_rule(color='red').encode(
        y='points:Q'
    )

    # Median line
    median_line = alt.Chart(pd.DataFrame({'points': [median_y]})).mark_rule(color='cyan', strokeDash=[2, 2]).encode(
        y='points:Q'
    )

    # mad_lines = alt.Chart(pd.DataFrame({'points': [mean_y - mad_y, mean_y + mad_y]})).mark_rule(color='orange', strokeDash=[5, 5]).encode(
    #     y='points:Q'
    # )
    chart = (line + dots + mean_line + median_line)#
    st.title(slug_to_name(player_key))
    st.altair_chart(chart,use_container_width=True)
    
    
player_selectbox = st.selectbox(
    "Player",
    playerList['players'],
    key='selected_option',
    format_func= slug_to_name,
    on_change=on_player_selectbox_change
)

st.write('You picked: ',player_selectbox)
showPlayerData(playerList['players'][0])