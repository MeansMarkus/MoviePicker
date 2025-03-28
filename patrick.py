import unittest
import json
from app import app  # Import your Flask app

class MovieRecommendationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_recommend_movie(self):
        # Simulate a POST request with a list of favorite movies
        favorite_movies = {
            'favorite_movies': ['Guardians of the Galaxy', 'Interstellar']
        }
        
        response = self.app.post('/recommend-movie', 
                                 data=json.dumps(favorite_movies),
                                 content_type='application/json')

        # Check if the response is valid and contains a recommendation
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('recommended_movie', data)
        self.assertIn('rating', data)
        print(f"Recommended Movie: {data['recommended_movie']}, Rating: {data['rating']}")

    def test_no_movies_to_recommend(self):
        # Simulate a POST request with all movies from the dataset to test no recommendation case
        all_favorite_movies = {
            'favorite_movies': ['Guardians of the Galaxy', 'Interstellar', 'The Godfather']  # Add all possible movie titles here
        }

        response = self.app.post('/recommend-movie', 
                                 data=json.dumps(all_favorite_movies),
                                 content_type='application/json')

        # Check if the response returns a 404 when no movies are available for recommendation
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()