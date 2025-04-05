import pandas as pd
import spotipy
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import csv
import unittest
import numpy as np
import app
import requests


data = pd.read_csv("dataset.csv") #read from dataset

song_var = [
    "danceability", "energy", "key", "loudness", "mode",
    "speechiness", "acousticness", "instrumentalness", 
    "liveness", "valence", "tempo", "time_signature"
] #numeric variables that we can compare
data[song_var] = data[song_var].apply(pd.to_numeric) #extract data

X = data[song_var].values

scaler = StandardScaler() #use standard scaler to standardized variables
X_scaled = scaler.fit_transform(X)

knn = NearestNeighbors(n_neighbors=5, metric='euclidean') #fit the nearest neighbor model to our dataset's data
knn.fit(X_scaled)

def get_nearest_songs(spot, track_id, access_token, n_neighbors=5):
#def get_nearest_songs(n_neighbors=5):
    track = get_track_data(spot, track_id, access_token)

    #song_data = np.array([0.676, 0.461, 1, -6.746, 0, 0.143, 0.0322, 1.01e-06, 0.358, 0.715, 87.917, 4]).reshape(1, -1)

    song_data = np.array([
        track["danceability"], track["energy"], track["key"],
        track["loudness"], track["mode"], track["speechiness"],
        track["acousticness"], track["instrumentalness"], 
        track["liveness"], track["valence"], track["tempo"],
        track["time_signature"]
    ]).reshape(1, -1) #put into array form

    song_data_scaled = scaler.transform(song_data) #scale song data using standardized scaler

    distances, indices = knn.kneighbors(song_data_scaled) #find nearest neighbors

    closest_songs = []

    for i, idx in enumerate(indices[0]):
        song_info = {
            "Track ID": data.iloc[idx]['track_id'],
            "Track Name": data.iloc[idx]['track_name'],
            "Artist": data.iloc[idx]['artists'],
            "Album Name": data.iloc[idx]['album_name'],
            "Distance": float(distances[0][i])
        }
        closest_songs.append(song_info)

    return closest_songs

def extract_from_dataset(track_data):
    return [
        float(track_data["danceability"]),
        float(track_data["energy"]),
        int(track_data["key"]),
        float(track_data["loudness"]),
        int(track_data["mode"]),
        float(track_data["speechiness"]),
        float(track_data["acousticness"]),
        float(track_data["instrumentalness"]),
        float(track_data["liveness"]),
        float(track_data["valence"]),
        float(track_data["tempo"]),
        int(track_data["time_signature"])
    ]

def get_track_data(spot, track_id, access_token):
    track = spot.track(track_id)
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    track_features = response.json()
    #artists = [artist['name'] for artist in track['artists']]
    print(track_features)

    track_details = {
        'track_id': track['id'], 
        #'artists': artists,
        #'album_name': track['album']['name'],
        #'track_name': track['name'],
        #'duration_ms': track['duration_ms'],
        #'explicit': track['explicit'],
        'danceability': track_features['danceability'],
        'energy': track_features['energy'],
        'key': track_features['key'],
        'loudness': track_features['loudness'],
        'mode': track_features['mode'],
        'speechiness': track_features['speechiness'],
        'acousticness': track_features['acousticness'],
        'instrumentalness': track_features['instrumentalness'],
        'liveness': track_features['liveness'],
        'valence': track_features['valence'],
        'tempo': track_features['tempo'],
        'time_signature': track_features['time_signature']
        #'track_genre': track_features['danceability'] #cant find genre in api for specific tracks
    }
    return track_details

def test_extract_from_dataset(): #unit test for extracting track data from current dataset
    track_data = data.iloc[0] 

    song_variables = extract_from_dataset(track_data)

    print("Extracted song variables:", song_variables)

def test_find_nearest_songs(access_token):
    print(access_token)
    sp = spotipy.Spotify(auth=access_token)
    closest_songs = get_nearest_songs(sp, "3n3Ppam7vgaVa1iaRUc9Lp", access_token) #random test with stairway to heaven

    print("Nearest songs:", closest_songs)

#test_extract_from_dataset()
#test_find_nearest_songs(access_token)