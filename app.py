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

def drawChart(df,player_key,data_label,lowerMax,upperMax):
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

    lowerRangeLine = alt.Chart(
        pd.DataFrame({
            'game':range(dimens[0]),
            'lower':[lowerMax]*dimens[0]
        }),
    ).mark_line(color='rgb(255, 75, 75)').encode(x='game',y='lower')

    chart = (line + dots + mean_line) #+ upperRangeLine + lowerRangeLine)#
    st.title(slug_to_name(player_key))
    st.altair_chart(chart,use_container_width=True)
    return chart
    

# with st.form("single-stat-form"):
st.session_state['data_label'] = 'pts'
st.session_state['lowerMax'] = 15
st.session_state['upperMax'] = 35

def slider_on_change():
    newLowerMax,newUpperMax = st.session_state['slider_vals']
    st.session_state['lowerMax'] = newLowerMax
    st.session_state['upperMax'] = newUpperMax

@st.fragment
def chart_fragment():
    player_key = st.session_state['player_key']
    data_label = st.session_state['data_label']
    df_stat = get_data_frame(player_key,data_label)
    # df_all = get_data_frame_all_stats(player_key)
    lowerMax = st.session_state['lowerMax']
    upperMax = st.session_state['upperMax']
    drawChart(df_stat,player_key,data_label,lowerMax,upperMax)
    
    st.slider(
        "Range ",
        0,
        50,
        (lowerMax,upperMax),
        key='slider_vals',
        on_change=slider_on_change
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

@st.cache_data 
def get_player_df(player_key):
    raw_json = server.get_player_data(player_key)
    dfMap = {}
    for stat,data in raw_json.items():
        if stat in ['name','_rev','_id','age','team_id']:
            continue
        dfMap[stat] = data
    # st.write(dfMap)
    return pd.DataFrame(dfMap)

def update_figure():
    newLowerMax,newUpperMax = st.session_state['slider_vals']
    
    st.session_state['lowerMax'] = newLowerMax
    st.session_state['upperMax'] = newUpperMax

    # fig.update_traces(,selector=dict(name="Lower Max"))

@st.fragment
def plotly_go_fragment():
    df = get_player_df('lauri-markkanen')
    # st.write(df)
    nGames = len(df['game_season'])
    st.session_state['nGames'] = nGames
    fig = go.Figure()
    mode = 'lines+markers'
    fig.add_trace(go.Scatter(
        name='Points',
        mode=mode,
        x=df['game_season'],
        y=df['pts']
    ))
    
    mean_pts = df['pts'].mean()

    fig.add_trace(go.Scatter(
        mode='lines',
        name='Avg Points',
        x=df['game_season'],
        y=[mean_pts] * nGames,
        line=dict(dash='dash')
    ))

    lowerMax = st.session_state['lowerMax']
    upperMax = st.session_state['upperMax']

    fig.add_trace(go.Scatter(
        mode='lines',
        name='Upper Max',
        x=df['game_season'],
        y=[upperMax] * nGames
    ))

    fig.add_trace(go.Scatter(
        mode='lines',
        name='Lower Max',
        x=df['game_season'],
        y=[lowerMax] * nGames
    ))

    fig.update_layout(
        xaxis=dict(title='Game',showgrid=True),
        yaxis=dict(title='Points',showgrid=True)
        )

    st.session_state['points_fig'] = fig

    st.plotly_chart(fig)


    values = st.slider(
        "Range ",
        0,
        45,
        (lowerMax,upperMax),
        key='slider_vals',
        on_change=update_figure
    )
    st.write("Values => ",values)

@st.fragment
def plotly_express_fragment():
    # df = pd.DataFrame({
    #     'game':[1,2,3,4],
    #     'points':[12,4,5,10]
    # })
    # raw_json = server.get_player_stats('tyler herro','pts')
    raw_json = server.get_player_data('tyler-herro')
    dfMap = {}
    for stat,data in raw_json.items():
        if stat in ['name','_rev','_id','age']:
            continue
        dfMap[stat] = data
    # st.write(dfMap)
    df = pd.DataFrame(dfMap)
    # df = pd.DataFrame({
    #     'game':range(1,len(points) + 1),
    #     'points':points,
    # })
    st.write(df)
    fig = px.line(df,x='game_season',y='trb',title='Plotly-HW',markers=True,labels={
        'game_season':'Game',
        'pts':'Points',
        'trb':'Total Rebounds'
        })
    st.write(fig)


# plotly_go_fragment()
# plotly_express_fragment()
main_fragment()

