import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, url_for, render_template

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key" #placeholder value since we're running locally

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"    #updated redirect_uri to function with flask

#initialize authentication for public data and user data
client_auth = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
user_auth = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    #add to scope when new permission necessary
    scope=["user-library-read", "playlist-modify-public", "user-read-playback-state", "user-modify-playback-state", "user-read-recently-played"]
)

#default route, initializes website and connect button with auth_url
@app.route("/")
def home():
    auth_url = user_auth.get_authorize_url()
    return render_template("website.html", auth_url=auth_url)

@app.route("/callback")
def callback():
    session.clear()
    code = request.args.get("code") #grabs auth code from spotify's redirect
    if code:
        token_info = user_auth.get_access_token(code)
        session["token_info"] = token_info #sets token for the session to save login info
        return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("home")) #redirects to home if no successful token found

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user_info = sp.current_user() #pulls user_info

    #eventually, this will redirect to a different dashboard page, but for now just
    #redirects to a html file with your username being displayed
    return f''' 
        <h1>Welcome, {user_info["display_name"]}</h1>
        <p>Spotify Connected Successfully!</p>
    '''

if __name__ == "__main__":
    app.run(debug=True) #runs app

'''
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
'''