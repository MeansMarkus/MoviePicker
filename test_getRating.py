import unittest

def getRating(rating):
    if not isinstance(rating, (int, float)):  # Accept both int and float types
        raise ValueError("Rating must be an integer or a float.")
    if rating < 1 or rating > 10:
        raise ValueError("Rating must be between 1 and 10.")
    return rating

class TestGetRating(unittest.TestCase):
    
    def test_edge_case_values(self):
        with self.assertRaises(ValueError):
            getRating(-1)  
        with self.assertRaises(ValueError):
            getRating(11)  

    def test_invalid_types(self):
        with self.assertRaises(ValueError):
            getRating("string")  
        with self.assertRaises(ValueError):
            getRating([5])  

    def test_valid_rating(self):
        for valid_rating in range(1, 11):
            self.assertEqual(getRating(valid_rating), valid_rating)
        for valid_float in [1.5, 5.5, 9.9]:  
            self.assertEqual(getRating(valid_float), valid_float)

if __name__ == '__main__':
    unittest.main()
