import unittest
import sys
import os


# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestMusicRecommendationApp(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test"""
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        """Test that the home page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Rhythm Finder", response.data)

    def test_songs_page(self):
        """Test that the songs recommendation page loads correctly"""
        response = self.client.get('/songs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Song Recommendations", response.data)

    def test_artists_page(self):
        """Test that the artists recommendation page loads correctly"""
        response = self.client.get('/artists')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Artist Recommendations", response.data)

    def test_genres_page(self):
        """Test that the genres recommendation page loads correctly"""
        response = self.client.get('/genres')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Genre Recommendations", response.data)

    def test_pages_have_navigation(self):
        """Test that pages have basic navigation elements"""
        pages = ['/', '/songs', '/artists', '/genres']
        
        for page in pages:
            response = self.client.get(page)
            self.assertEqual(response.status_code, 200)
            
            # Check for navigation elements
            navigation_items = [
                b"Song Recommendations", 
                b"Artist Recommendations", 
                b"Genre Recommendations",
                b"Back to Home"
            ]
            
            for item in navigation_items:
                self.assertIn(item, response.data)

if __name__ == '__main__':
    unittest.main()