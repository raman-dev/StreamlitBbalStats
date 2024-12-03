import requests

class DataServer:
    PLAYER_URL='http://localhost:5984/players'
    ALL_PLAYERS_VIEW = '/_design/allPlayers/_view/all-players-view'
    POINTS_VIEW = '/_design/allPlayers/_view/points-view'
    REBOUNDS_VIEW = '/_design/allPlayers/_view/rebounds-view'

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

    def get_player_rebounds(self,player):
        url = DataServer.PLAYER_URL +DataServer.REBOUNDS_VIEW+ f'/?key="{player}"'
        print(url)
        response = requests.get(url)
        raw_data = response.json()
        return raw_data['rows'][0]['value']
