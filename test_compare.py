import unittest
import pandas as pd
import random
from flask import Flask, jsonify, request

def recommend_movies(favorite_movies, movies_df, num_recommendations=2):
    """
    Simple movie recommendation function
    
    Args:
    - favorite_movies (list): List of favorite movie titles
    - movies_df (pd.DataFrame): DataFrame containing movie information
    - num_recommendations (int): Number of movies to recommend
    
    Returns:
    list: Recommended movie titles
    """
    # Basic input validation
    if not isinstance(favorite_movies, list):
        raise ValueError("Favorite movies must be a list")
    
    if len(favorite_movies) == 0:
        raise ValueError("At least one favorite movie is required")
    
    # Simple recommendation logic
    recommended = []
    
    for movie in favorite_movies:
        # Check if movie exists in the dataframe
        movie_matches = movies_df[movies_df['Title'].str.contains(movie, case=False)]
        
        if not movie_matches.empty:
            # Add a few movies from the same rating range
            rating = movie_matches.iloc[0]['Rating']
            
            # Find movies within 1 point of rating
            similar_movies = movies_df[
                (movies_df['Rating'].between(rating - 1, rating + 1)) & 
                (~movies_df['Title'].isin(favorite_movies + recommended))
            ]
            
            # Add top recommendations
            recommended.extend(similar_movies['Title'].head(num_recommendations).tolist())
    
    # Limit and deduplicate recommendations
    return list(dict.fromkeys(recommended))[:num_recommendations]

class TestMovieRecommendationSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load movie data before running tests
        cls.movies_df = pd.read_csv('IMDB-Movie-Data.csv')
    
    def test_recommend_movies_basic_functionality(self):
        """
        Basic test to ensure recommendations work
        """
        favorite_movies = ['The Dark Knight']
        recommendations = recommend_movies(favorite_movies, self.movies_df)
        
        # Basic checks
        self.assertIsInstance(recommendations, list)
        self.assertTrue(0 <= len(recommendations) <= 2)
        
        # Ensure recommendations don't include favorite movies
        for movie in favorite_movies:
            for rec in recommendations:
                self.assertNotEqual(movie.lower(), rec.lower())
    
    def test_recommend_movies_multiple_favorites(self):
        """
        Test recommendations with multiple favorite movies
        """
        favorite_movies = ['The Dark Knight', 'Inception']
        recommendations = recommend_movies(favorite_movies, self.movies_df)
        
        # Checks
        self.assertIsInstance(recommendations, list)
        self.assertTrue(0 <= len(recommendations) <= 2)
        
        # Ensure no duplicates in recommendations
        self.assertEqual(len(recommendations), len(set(recommendations)))
    
    def test_recommend_movies_input_validation(self):
        """
        Test input validation
        """
        # Test empty list
        with self.assertRaises(ValueError):
            recommend_movies([], self.movies_df)
        
        # Test non-list input
        with self.assertRaises(ValueError):
            recommend_movies('Not a list', self.movies_df)
    
    def test_recommend_movies_nonexistent_movie(self):
        """
        Test behavior with movies not in database
        """
        favorite_movies = ['Nonexistent Movie']
        recommendations = recommend_movies(favorite_movies, self.movies_df)
        
        # Should return an empty list
        self.assertEqual(len(recommendations), 0)

if __name__ == '__main__':
    unittest.main()