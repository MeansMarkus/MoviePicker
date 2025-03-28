import unittest

def filterAgeMovieRating(movies, ratings): #Filters movies by age content rating
    "Filters movies by age content rating"
    return [movie for movie in movies if movie.get("rating") in ratings]

class AgeRatingContent(unittest.TestCase): #Example of age content ratings

    def setUp(self):
        self.movies = [
            {"title": "Family", "rating": "G"},
            {"title": "Adventure", "rating": "PG-13"},
            {"title": "Horror", "rating": "R"},
            {"title": "Adult", "rating": "NC-17"}
        ]

    def testAllowedRatings(self): #Test for allowed ratings
        allowed_ratings = ["G", "PG", "PG-13"]
        filtered = filterAgeMovieRating(self.movies, allowed_ratings)
        self.assertEqual(len(filtered), 2)
        for movie in filtered:
            self.assertIn(movie["rating"], allowed_ratings)

    def testValidRating(self): #Test when the user doesn't choose to filter a rating
        allowed_ratings = []
        filtered = filterAgeMovieRating(self.movies, allowed_ratings)
        self.assertEqual(filtered, []) #No movies should be returned

    def testAllRatings(self): #Test when the user wants all ratings
        allowed_ratings = ["G", "PG-13", "R", "NC-17"]
        filtered = filterAgeMovieRating(self.movies, allowed_ratings)
        self.assertEqual(filtered, self.movies)

if __name__ == "__main__":
    unittest.main()
