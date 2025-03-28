import unittest
import json
from app import app  # Assuming your main file is named app.py
import pandas as pd

class TestMovieRandomEndpoint(unittest.TestCase):
    def setUp(self):
        """
        Set up test client and load test data
        """
        self.app = app.test_client()
        self.movies_df = pd.read_csv('IMDB-Movie-Data.csv')
    
    def test_get_random_movie_endpoint(self):
        """
        Test the /get-random-movie endpoint
        """
        # Send request to the endpoint
        response = self.app.get('/get-random-movie')
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = json.loads(response.data)
        
        # Validate response structure
        self.assertIn('title', data)
        self.assertIn('rating', data)
        
        # Verify the movie exists in the original dataset
        self.assertIn(data['title'], self.movies_df['Title'].values)
    
    def test_random_movie_rating_type(self):
        """
        Ensure the rating is a float or int
        """
        response = self.app.get('/get-random-movie')
        data = json.loads(response.data)
        
        # Check rating is a number
        self.assertIsInstance(data['rating'], (int, float))
    
    def test_multiple_random_movie_calls(self):
        """
        Verify that multiple calls can return different movies
        """
        # Make multiple calls and collect results
        movies = set()
        for _ in range(10):
            response = self.app.get('/get-random-movie')
            data = json.loads(response.data)
            movies.add(data['title'])
        
        # Ensure we got more than one unique movie
        self.assertTrue(len(movies) > 1, "Multiple calls should return different movies")

    def test_home_route(self):
        """
        Test the home route serves the index.html file
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()