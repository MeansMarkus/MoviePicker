import unittest
class AgeRatingContent(unittest.TestCase): 

    def filterAgeMovieRating(movies, ratings): #Filters movies by age content rating
        "Filters movie by age content rating"
        return [movie for movie in movies if movie.get["rating"] in ratings]
        
    def ageContentRatings(self): #Example of age content ratings
        self.movies = [{"title" : "Family" , "rating" : "G"} , 
       {"title" : "Adventure" , "rating" : "PG-13"}, 
       {"title" : "Horror" , "rating" : "R"},
       {"title" : "Adult" , "rating" : "NC-17"}]
        
    def testAllowedRatings(self): #Test for allowed ratings
        allowed_rating = ["G", "PG", "PG-13"]
        filtered = self.filterAgeMovieRating(self.movies, allowed_rating)

        for movie in filtered:
            self.assertIn(movie("rating"), allowed_rating)
            self.assertEqual(len(filtered), 3)

    def testValidRating(self): #Test when the user doesn't choose to filter a rating
        allowed_rating = []
        filtered = filterAgeMovieRating(self.movies, allowed_rating)
        self.assertEqual(filtered, []) #No movies should be returned

    def testAllRatings(self): #Test when the user wants all ratings
        allowed_rating = ["G", "PG", "PG-13", "R", "NC-17"]
        filtered = filterAgeMovieRating(self.movies, allowed_rating)
        self.assertEqual(filtered, self.movies)

    if __name__ == "__main__":
        unittest.main()




