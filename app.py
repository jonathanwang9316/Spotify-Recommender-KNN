import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, url_for, render_template
import recommend

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
    scope=["user-library-read", "playlist-modify-public", "user-read-playback-state", "user-modify-playback-state", "user-read-recently-played", "user-read-private", "user-read-email", "user-top-read"]
)

#default route, initializes website and connect button with auth_url
@app.route("/")
def home():
    auth_url = user_auth.get_authorize_url()
    print(auth_url)
    return render_template("Simple_Website.html", auth_url=auth_url)

@app.route("/callback")
def callback():
    session.clear()
    code = request.args.get("code") #grabs auth code from spotify's redirect
    if code:
        token_info = user_auth.get_access_token(code)
        session["token_info"] = token_info #sets token for the session to save login info
        return redirect(url_for("songs", time_range="medium_term"))
    else:
        return redirect(url_for("home"))


@app.route("/songs/<time_range>")
def songs(time_range):
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("home")) #redirects to home if no successful token found
    if time_range not in ['short_term', 'medium_term', 'long_term']:
        time_range = "short_term" #default term to short_term
    access_token = refresh_token() or token_info["access_token"]
    print(access_token)
    print(token_info["refresh_token"])
    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.current_user() #pulls user_info
    user_top_tracks = get_top_5_tracks(access_token, time_range=time_range)

    #song_rec_url = search_song(song_name= song_rec["song_name"], artist= song_rec["artist"])
    recommended_tracks = recommend.get_nearest_songs(user_top_tracks)
    song_rec_urls = []
    seen_urls = set()

    for rec in recommended_tracks:
        curr_url = search_song(song_name = rec[0], artist= rec[1])
        if curr_url != "No results found." and curr_url not in seen_urls: #ensures song was actually found on Spotify
            song_rec_urls.append(curr_url)
            seen_urls.add(curr_url)

        if len(song_rec_urls) == 5: #stops once we have 5 urls
            break

    return render_template("songs.html", user_name = user_info["display_name"],
                           song_rec_url_1 = song_rec_urls[0], song_rec_url_2 = song_rec_urls[1],
                           song_rec_url_3 = song_rec_urls[2], song_rec_url_4 = song_rec_urls[3],
                           song_rec_url_5 = song_rec_urls[4])

@app.route("/genres")
def genres():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("home")) #redirects to home if no successful token found

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user_info = sp.current_user() #pulls user_info

    return render_template("genres.html", user_name = user_info["display_name"])

@app.route("/artists")
def artists():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("home")) #redirects to home if no successful token found

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user_info = sp.current_user() #pulls user_info

    #eventually, this will redirect to a different dashboard page, but for now just
    #redirects to a html file with your username being displayed
    return render_template("artists.html", user_name = user_info["display_name"])

#function that searches for a song on spotify based on supabase information
def search_song(song_name, artist):
    query = f"track:{song_name}"
    query += f" artist:{artist}"

    results = client_auth.search(q=query, type='track', limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        #generates embed version of url from standard url
        standard_url = track['external_urls']['spotify']
        track_id = standard_url.split("track/")[1]
        return f"https://open.spotify.com/embed/track/{track_id}"

    else:
        return "No results found."

def refresh_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return None

    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        # add to scope when new permission necessary
        scope=["user-library-read", "playlist-modify-public", "user-read-playback-state", "user-modify-playback-state",
               "user-read-recently-played", "user-read-private", "user-top-read"]
    )
    new_token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

    # Update session with the new token
    session["token_info"] = new_token_info
    return new_token_info["access_token"]

def get_top_5_tracks(access_token, time_range): #pulls the users top 5 tracks from the past month
    sp = spotipy.Spotify(auth=access_token)
    results = sp.current_user_top_tracks(limit=5, time_range=time_range)
    track_ids = [track["id"] for track in results["items"]]
    return track_ids

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