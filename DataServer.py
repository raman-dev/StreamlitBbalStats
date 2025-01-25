import requests
import json 

class DataServer:
    PLAYER_URL='http://localhost:5984/players'
    ALL_PLAYERS_VIEW = '/_design/allPlayers/_view/all-players-view'
    POINTS_VIEW = '/_design/allPlayers/_view/points-view'
    REBOUNDS_VIEW = '/_design/allPlayers/_view/rebounds-view'

    def get_players(self):
        #use requests library to request from the data server
        response = requests.get(DataServer.PLAYER_URL + DataServer.ALL_PLAYERS_VIEW)
        data = response.json()
        return {'players':[x['id'] for x in data['rows']], 'count':data['total_rows']}#count

    def get_teams(self):
        response = requests.get(DataServer.)
        return {}
    
    def get_player_data(self,player):
        response = requests.get(DataServer.PLAYER_URL + f'/{player}')
        #drop revision id and id
        data = response.json()
        dropDataMappings = ['_id','_rev','name','age']
        for x in dropDataMappings:
            data.pop(x)
        return data
    
    def get_player_stat(self,name,stat):
        body = {
            'selector' :{'name':name},
            'fields': [stat]
        }
        headers = {'Content-Type':'application/json'}
        response = requests.post(
            url=DataServer.PLAYER_URL + f'/_find',
            headers=headers,
            data=json.dumps(body))
        data = response.json()
        return data
    
    def get_stats_available(self):
        response = requests.get(DataServer.PLAYER_URL + '/stats-info')
        return response.json()['stats-available']

