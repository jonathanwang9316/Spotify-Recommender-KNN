import pandas as pd
import spotipy
#from spotify_authentication import user_auth

#spot = spotipy.Spotify(auth_manager=user_auth)

def get_track_data(spot, track_id):
    track = spot.track(track_id)
    track_features = spot.audio_features(track_id)[0]

    artists = [artist['name'] for artist in track['artists']]

    track_details = {
        'track_id': track['id'], 
        'artists': artists,
        'album_name': track['album']['name'],
        'track_name': track['name'],
        'duration_ms': track['duration_ms'],
        'explicit': track['explicit'],
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