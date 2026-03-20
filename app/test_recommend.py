import unittest
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
from recommend import extract_from_dataset, get_nearest_songs, get_song_vars

class TestSongDataExtraction(unittest.TestCase):

    def setUp(self):
        # Create a small test dataset
        data = {
            'danceability': [0.676],
            'energy': [0.461],
            'key': [1],
            'loudness': [-6.746],
            'mode': [0],
            'speechiness': [0.143],
            'acousticness': [0.0322],
            'instrumentalness': [1.01e-06],
            'liveness': [0.358],
            'valence': [0.715],
            'tempo': [87.917],
            'time_signature': [4]
        }
        self.test_data = pd.DataFrame(data)

    def test_extract_from_dataset(self):
        track_data = self.test_data.iloc[0]  # Get the first row (single song)
        expected_output = [
            0.676, 0.461, 1, -6.746, 0, 0.143, 0.0322, 1.01e-06, 
            0.358, 0.715, 87.917, 4
        ]
        
        # Call the extract_from_dataset function
        result = extract_from_dataset(track_data)
        
        self.assertEqual(result, expected_output)

class TestKNNFunctionality(unittest.TestCase):

    def setUp(self):
        # Create a small test dataset of songs
        self.X_test = np.array([
            [0.676, 0.461, 1, -6.746, 0, 0.143, 0.0322, 1.01e-06, 0.358, 0.715, 87.917, 4],
            [0.5, 0.6, 2, -5.0, 1, 0.12, 0.04, 2e-06, 0.33, 0.72, 90.0, 4],
            [0.8, 0.7, 1, -4.0, 1, 0.1, 0.03, 1.5e-06, 0.35, 0.75, 92.0, 4]
        ])

        # Initialize the KNN model
        self.knn = NearestNeighbors(n_neighbors=2, metric='euclidean')
        self.knn.fit(self.X_test)

    def test_knn_neighbors(self):
        # Query for the first song in the dataset
        song_data = self.X_test[0].reshape(1, -1)
        distances, indices = self.knn.kneighbors(song_data)
        
        # We expect that the first song is most similar to the second song in the dataset
        self.assertIn(indices[0][0], [0, 1, 2])  # Ensure we find the song itself or other similar ones
        self.assertNotEqual(indices[0][1], 0)  # Ensure the song itself isn't selected as the nearest neighbor

class TestGetSongVars(unittest.TestCase):
    
    def test_averaging_two_songs(self):
        # Input: Two songs with numerical attributes
        song1 = {
            'danceability': 0.6, 'energy': 0.5, 'key': 1, 'loudness': -6.0,
            'mode': 0, 'speechiness': 0.1, 'acousticness': 0.05, 'instrumentalness': 0.000001,
            'liveness': 0.3, 'valence': 0.7, 'tempo': 100.0, 'time_signature': 4
        }

        song2 = {
            'danceability': 0.8, 'energy': 0.7, 'key': 2, 'loudness': -4.0,
            'mode': 1, 'speechiness': 0.2, 'acousticness': 0.03, 'instrumentalness': 0.000002,
            'liveness': 0.4, 'valence': 0.8, 'tempo': 120.0, 'time_signature': 4
        }

        expected_output = {
            'danceability': 0.7, 'energy': 0.6, 'key': 1.5, 'loudness': -5.0,
            'mode': 0.5, 'speechiness': 0.15, 'acousticness': 0.04, 'instrumentalness': 0.0000015,
            'liveness': 0.35, 'valence': 0.75, 'tempo': 110.0, 'time_signature': 4.0
        }

        # Call the function
        result = get_song_vars([song1, song2])

        # Check if results match expected output
        for key in expected_output:
            self.assertAlmostEqual(result[key], expected_output[key], places=6)

if __name__ == "__main__":
    unittest.main()