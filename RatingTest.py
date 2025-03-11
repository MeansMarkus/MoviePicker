import unittest

# Assume getRating function is defined somewhere (mock implementation for now)
def getRating(rating):
    if not isinstance(rating, (int, float)):  # Accept both int and float types
        raise ValueError("Rating must be an integer or a float.")
    if rating < 1 or rating > 10:
        raise ValueError("Rating must be between 1 and 10.")
    return rating

class TestGetRating(unittest.TestCase):
    
    def test_edge_case_values(self):
        # Test for boundary conditions (negative and > 10)
        with self.assertRaises(ValueError):
            getRating(-1)  # Negative value
        with self.assertRaises(ValueError):
            getRating(11)  # Value greater than 10
    
    def test_invalid_types(self):
        # Test for invalid types (non-integer, non-float)
        with self.assertRaises(ValueError):
            getRating("string")  # Invalid type, should be int or float
        with self.assertRaises(ValueError):
            getRating([5])  # Invalid type, should be int or float
    
    def test_valid_rating(self):
        # Test for valid ratings between 1 and 10 (inclusive), both integer and float
        for valid_rating in range(1, 11):
            self.assertEqual(getRating(valid_rating), valid_rating)
        for valid_float in [1.5, 5.5, 9.9]:  # Test with float values
            self.assertEqual(getRating(valid_float), valid_float)

if __name__ == '__main__':
    unittest.main()
