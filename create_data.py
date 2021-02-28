import numpy as np
import pandas as pd
import spotipy
import json
from os import listdir
from tqdm import tqdm


# GET ACCESS TOKEN
with open('auth_info.json') as f: 
    auth_info = json.load(f) 
def get_token(a=auth_info):
    token = spotipy.util.prompt_for_user_token(username=a['username'], 
                                   scope=a['scope'], 
                                   client_id=a['client_id'],   
                                   client_secret=a['client_secret'],     
                                   redirect_uri=a['redirect_uri'])
    return token
token = get_token()

# LOAD STREAMING HISTORY INTO PANDAS DATAFRAME
files_path = list(map(lambda file_name: 'data/input/' + file_name, listdir('data/input/')))
data = pd.DataFrame([])
for file_path in files_path: 
    with open(file_path, encoding='UTF-8') as f:
        data = data.append(pd.read_json(f), ignore_index=True)


"""Get the track ID given the track name and artist name.

Args:
    key (str): key is track name + artist name

Returns:
    str: returns a string of track ID retrived from the Spotify API, returns none if no match
"""

def get_track_id(key: str):
    global token
    spotify = spotipy.Spotify(auth=token)
    key = key.split('+')
    track_name = key[0].split('(')[0].split('-')[0] # remove bracket content & - content in track name
    artist_name = key[1] 
    key = track_name+ ' AND ' + artist_name
    search_round_limit = 5
    while search_round_limit != 0:
        search_round_limit -= 1
        try:
            result = spotify.search(key, limit=1)
            result_item = result['tracks']['items']
            if len(result_item):
                return result['tracks']['items'][0]['id']
            else:
                continue
        except spotipy.client.SpotifyException:
            token = get_token(auth_info)
            spotify = spotipy.Spotify(auth=token)
            print("Refreshed token.")
        except:
            return None
    if not search_round_limit:
        return None

# ADD ID COLUMN TO STREAMING DATAFRAME
data.insert(0, "trackId", data["trackName"]+'+'+data["artistName"])
tqdm.pandas()
data["trackId"] = data["trackId"].progress_apply(get_track_id)

# WRITE TO FILE 'streaming_history_with_track_id.json'
data.to_json(r'data/output/streaming_history_with_track_id.json')


"""Get the track features given the track ID.

Args:
    track_id (str): track ID of a track

Returns:
    dict: returns a dictionary containing features of a track
    features are 'danceability','energy','key','loudness','mode','speechiness','acousticness',
    'instrumentalness','liveness','valence','tempo','id','duration_ms','time_signature',
    'popularity'
"""

def get_track_features(track_id: str):
    global token
    spotify = spotipy.Spotify(auth=token)
    search_round_limit = 5
    while search_round_limit != 0:
        search_round_limit -= 1
        try:
            spotify = spotipy.Spotify(auth=token)
            track_features = spotify.audio_features([track_id])[0]
            track_info = spotify.track(track_id)
            track_pop = track_info['popularity']
            track_features['popularity'] = track_pop
            track_features.pop('track_href')
            track_features.pop('analysis_url')
            track_features.pop('uri')
            track_features.pop('type')
            track_features.pop('id')
            return list(track_features.values())
        except spotipy.client.SpotifyException:
            token = get_token(auth_info)
            spotify = spotipy.Spotify(auth=token)
            print("Refreshed token.")
        except:
            None

with open('data/output/streaming_history_with_track_id.json', encoding='UTF-8') as f:
        data = pd.read_json(f)

# INITIALIZE FEATURE COLUMNS
features = [
    'danceability',
     'energy',
     'key',
     'loudness',
     'mode',
     'speechiness',
     'acousticness',
     'instrumentalness',
     'liveness',
     'valence',
     'tempo',
     'id',
     'duration_ms',
     'time_signature',
     'popularity'
]
data[features] = None

n = len(data)
for i in tqdm(range(n)):
    track_id = data['trackId'][i]
    if not None: 
        data.iloc[i, 5:] = get_track_features(track_id)
    else: 
        print("Track "+ i + "with ID "+track_id+" features cannot be obtained.")

# WRITE TO FILE 'streaming_history_with_track_id_and_features.json'
data.to_json(r'data/output/streaming_history_with_track_id_and_features.json')


