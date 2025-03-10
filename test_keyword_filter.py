import unittest
from keyword_filter import checkKeyword

descriptions = ["action movie about two superheroes that have magic powers that have 1 goal", "cómo se dice"]

class TestKeywordValidation(unittest.TestCase):
    def test_valid_single_word(self):
        self.assertTrue(checkKeyword("superheroes", descriptions))
    def test_valid_part_of_word(self):
        self.assertTrue(checkKeyword("superhero", descriptions))
    def test_valid_incorrect_capitalization(self):
        self.assertTrue(checkKeyword("mAGiC", descriptions))
    def test_invalid_empty_string(self):
        self.assertFalse(checkKeyword("", descriptions))
    def test_invalid_null_string(self):
        self.assertFalse(checkKeyword(None, descriptions))
    def test_invalid_dne(self):
        self.assertFalse(checkKeyword("asdf", descriptions))
    def test_edge_case_with_numerals(self):
        self.assertTrue(checkKeyword("2", descriptions))
    def test_edge_case_with_spelled_nums(self):
        self.assertTrue(checkKeyword("one", descriptions))
    def test_edge_case_with_diacritic(self):
        self.assertTrue(checkKeyword("cómo", descriptions))
    def test_edge_case_with_punctuation(self):
        self.assertTrue(checkKeyword("magic!", descriptions))  
    def test_edge_case_with_symbols(self):
        self.assertTrue(checkKeyword("a@ction:", descriptions))
    def test_edge_case_with_multiple_words(self):
        self.assertTrue(checkKeyword("magic powers", descriptions))

if __name__ == '__main__':
    unittest.main()