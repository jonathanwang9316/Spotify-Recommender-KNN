import unittest
from app import app, search_song
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
import html

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

load_dotenv()

user_auth = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    #add to scope when new permission necessary
    scope=["user-library-read", "playlist-modify-public", "user-read-playback-state", "user-modify-playback-state", "user-read-recently-played"]
)

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up test client"""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = app.test_client()

    def test_home_route(self):
        """Test if home route loads correctly"""
        response = self.client.get('/')
        expected_url = user_auth.get_authorize_url()
        rendered_url = response.data.decode()
        rendered_url = html.unescape(rendered_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_url, rendered_url)  # Check if auth_url is in response

    def test_callback_no_code(self):
        """Test callback route with no auth code"""
        response = self.client.get('/callback')
        self.assertEqual(response.status_code, 302)  # Should redirect to home
        self.assertIn(b'/', response.location.encode())

    def test_songs_no_token(self):
        """Test songs route without a valid token"""
        response = self.client.get('/songs')
        self.assertEqual(response.status_code, 302)  # Should redirect to home
        self.assertIn(b'/', response.location.encode())

    def test_search_song_no_results(self):
        """Test search_song function with no results"""
        result = search_song("NonExistentSong", "NonExistentArtist")
        self.assertEqual(result, "No results found.")


if __name__ == "__main__":
    unittest.main()
