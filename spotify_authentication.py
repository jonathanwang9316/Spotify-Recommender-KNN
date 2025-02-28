import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "127.0.0.1/callback"

#initialize authentication for public data and user data
client_auth = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
user_auth = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    #add to scope when new permission necessary
    scope=["user-library-read", "playlist-modify-public", "user-read-playback-state", "user-modify-playback-state", "user-read-recently-played"]
))

#gets the users 10 most recently played tracks
def get_user_recent_tracks():
    results = user_auth.current_user_recently_played(limit=10)
    recent_tracks = []

    for idx, item in enumerate(results['items']):
        track = item['track']
        track_info = f"{idx+1}: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}"
        recent_tracks.append(track_info)

    return recent_tracks

print("\nFetching user's 10 most recently played tracks...")
user_recent_tracks = get_user_recent_tracks()
for user_track in user_recent_tracks:
    print(user_track)