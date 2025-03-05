import unittest
class AgeRatingContent(unittest.TestCase): 


    def filterAgeMovieRating(movies, ratings):
        "Filters movie by age content rating"
        return [movie for movie in movies if movie.get["rating"] in ratings]
        
    def ageContentRatings(self):
        self.movies = [{"title" : "Family" , "rating" : "G"} , 
       {"title" : "Adventure" , "rating" : "PG-13"}, 
       {"title" : "Horror" , "rating" : "R"},
       {"title" : "Adult" , "rating" : "NC-17"}]
        
    def testAllowedRatings(self):
        allowed_rating = ["G", "PG", "PG-13"]
        filtered = filterAgeMovingRating
    def test_valid_rating(self):
        rating = "PG"
        self.assertEqual(getMovieRating(rating), "PG")

    def test_invalid_rating(self):
        rating = "XYZ"
        self.assertFalse(getMovieRating(rating), "XYZ")

    def testRuleRating(self):
        rating = getMovieRating(movie)
        self.assertTrue(rating)


