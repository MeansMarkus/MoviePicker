import unittest
class AgeRatingContent(unittest.TestCase):

    def test_valid_rating(self):
        rating = "PG"
        self.assertEqual(getMovieRating(rating), "PG")

    def test_invalid_rating(self):
        rating = "XYZ"
        self.assertFalse(getMovieRating(rating), "XYZ")

    def testRuleRating(self):
        rating = getMovieRating(movie)
        self.assertTrue(rating)

