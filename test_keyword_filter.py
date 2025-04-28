import unittest
from keyword_filter import checkKeyword

movies = [
    {
        "name": "Movie 1",
        "description": "action movie about superheroes that have magic powers"
    },
    {
        "name": "Movie Two",
        "description": "cómo se dice"
    }
]
class TestKeywordValidation(unittest.TestCase):
    def test_valid_single_word(self):
        self.assertTrue(checkKeyword("superheroes", movies))
    def test_valid_part_of_word(self):
        self.assertTrue(checkKeyword("superhero", movies))
    def test_valid_incorrect_capitalization(self):
        self.assertTrue(checkKeyword("mAGiC", movies))
    def test_invalid_empty_string(self):
        self.assertFalse(checkKeyword("", movies))
    def test_invalid_null_string(self):
        self.assertFalse(checkKeyword(None, movies))
    def test_invalid_dne(self):
        self.assertFalse(checkKeyword("asdf", movies))
    def test_edge_case_with_numerals(self):
        self.assertTrue(checkKeyword("1", movies))
    def test_edge_case_with_spelled_nums(self):
        self.assertTrue(checkKeyword("two", movies))
    def test_edge_case_with_diacritic(self):
        self.assertTrue(checkKeyword("cómo", movies))
    def test_edge_case_with_punctuation(self):
        self.assertTrue(checkKeyword("magic!", movies))  
    def test_edge_case_with_symbols(self):
        self.assertTrue(checkKeyword("a@ction:", movies))
    def test_edge_case_with_multiple_words(self):
        self.assertTrue(checkKeyword("magic powers", movies))

if __name__ == '__main__':
    unittest.main()