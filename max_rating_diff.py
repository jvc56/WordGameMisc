import requests
import sys

# Get maximum available game ID
max_game_id_url = 'http://cross-tables.com/rest/info.php'
max_game_id_headers = {'User-Agent': 'My User Agent'}
max_game_id_response = requests.get(max_game_id_url, headers=max_game_id_headers)

if max_game_id_response.ok:
    max_game_id = int(max_game_id_response.json()['maxgameid'])
else:
    print(f"Request for max game ID failed with status code {max_game_id_response.status_code}")
    sys.exit()

# Analyze all games in the API, 500 at a time
url = 'http://cross-tables.com/rest/games.php'
min_game_id = 1
max_game_id_chunk = min(500, max_game_id)

max_diff = 0
max_game = None

while min_game_id <= max_game_id:
    params = {'minid': min_game_id, 'maxid': max_game_id_chunk}
    headers = {'User-Agent': 'My User Agent'}
    print("request: %s - %s" % (params['minid'], params['maxid']))
    response = requests.get(url, params=params, headers=headers)

    if response.ok:
        games = response.json()['games']
        
        for game in games:
            winner_rating = int(game['winneroldrating'])
            loser_rating = int(game['loseroldrating'])
            diff = abs(winner_rating - loser_rating)
            if diff > max_diff:
                max_diff = diff
                max_game = game
                
        min_game_id += 500
        max_game_id_chunk = min(max_game_id_chunk + 500, max_game_id)
    else:
        print(f"Request for games failed with status code {response.status_code}")
        sys.exit()

print(f"Game with max difference: {max_game['gameid']}")
