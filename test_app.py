import unittest
from app import app, search_song
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from urllib.parse import urlparse
from bs4 import BeautifulSoup
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
    scope=["user-library-read", "playlist-modify-public", "user-read-playback-state", "user-modify-playback-state", "user-read-recently-played", "user-read-private", "user-read-email", "user-top-read"]
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
        response = self.client.get('/songs/short_term')
        self.assertEqual(response.status_code, 302)  # Should redirect to home
        self.assertIn(b'/', response.location.encode())

    def test_search_song_no_results(self):
        """Test search_song function with no results"""
        result = search_song("NonExistentSong", "NonExistentArtist")
        self.assertEqual(result, "No results found.")

    def test_recommendation_cards_unique_and_valid(self):
        """Test that the 5 recommendation cards have valid and unique Spotify URLs"""

        with self.client.session_transaction() as sess:
            # Mock session with a valid token
            sess["token_info"] = { #access_token and refresh_token need to be updated with valid current tokens to test properly
                "access_token": "BQCYdR7Uqo7xu7eirvs78lCpcNaup-Z2WhnOgkJLSgMwXqWGEPv4dQ62B_9WxaMcGsmytFDZXhSAIhkslK7hkrsWOhZjGgCVImUUmNxDr-eVYdkX4WyNIIM-S-NGFWfa6gJrfo082UOopmLOj1sDorkvvJAsjs7mDuhJi_JiX30IgEwv7uHCAXxPNIxAAORhx3o1You_dXrlO947e9tEDPqNkcmpPX93s2ZPqpyksiMrnvaCMt0b2kvl9GjNeDvMT4-DNQm7nutsY3FFgTxwsCpwUVCetP3opbPw8TwiEgn7qBeA",
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "user-top-read",
                "expires_at": 9999999999,
                "refresh_token": "AQDDQ6sMLBhT3PLuIEeFPnt_XjCh16O9RlI_YBs8ZiQD5BYi4Cf1JL4RZiEHTeWcCWoDlWeGOw30IYk4X_Gv8pxaC-YvHIYUs9utcYLyjIg9GAjxxVVny7ZJS46wAl1ZSeE"
            }

        response = self.client.get("/songs/short_term")
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.data, 'html.parser')

        # Find all recommendation-card elements and extract <iframe> srcs
        cards = soup.find_all(class_="recommendation-card")
        self.assertEqual(len(cards), 5, "Expected 5 recommendation cards")

        urls = []
        for card in cards:
            iframe = card.find("iframe")
            self.assertIsNotNone(iframe, "Missing iframe in recommendation card")
            src = iframe.get("src")
            self.assertIsNotNone(src, "Missing src in iframe")
            urls.append(src)

        # Ensure all URLs are valid
        for url in urls:
            parsed = urlparse(url)
            self.assertTrue(parsed.scheme in ["http", "https"] and parsed.netloc, f"Invalid URL: {url}")

        # Ensure all URLs are unique
        self.assertEqual(len(urls), len(set(urls)), "Duplicate URLs found in recommendations")

    def test_valid_time_ranges(self): #makes sure all different term urls are functional
        for term in ['short_term', 'medium_term', 'long_term']:
            response = self.client.get(f'/songs/{term}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_invalid_time_ranges_defaults_to_short(self):
        short_term_response = self.client.get('/songs/short_term')
        short_term_data = short_term_response.get_data(as_text=True)

        invalid_response = self.client.get('/songs/not_a_real_term', follow_redirects=True)
        invalid_data = invalid_response.get_data(as_text=True)

        self.assertEqual(invalid_response.status_code, 200)
        self.assertIn('short_term', invalid_response.get_data(as_text=True)) #tests if an invalid term input correctly defaults to short_term link


if __name__ == "__main__":
    unittest.main()
