import unittest
import tkinter as tk
from tkinter import simpledialog
from unittest.mock import patch

# This creates a pop up
def ask_for_age():
    # Creates the window pop up
    root = tk.Tk()
    root.withdraw()

    # Asks for age of the user/parameters of possible answers
    age = simpledialog.askinteger("Movie Picker", "What is your age?", parent=root, minvalue=0, maxvalue=120)

    # Clean up
    root.destroy()
    return age

# UnitTest using mock UI to automate the manual input that would be required for testing
class TestAge(unittest.TestCase):
    # Test for if user is 18/adult
    @patch('tkinter.simpledialog.askinteger', return_value=18)
    def test_adult_age(self, mock_askinteger):
        age = ask_for_age()
        self.assertEqual(age, 18)
        self.assertTrue(age >= 17, "User is an adult.")

    # Test for if user is 16/minor
    @patch('tkinter.simpledialog.askinteger', return_value=16)
    def test_minor_age(self, mock_askinteger):
        age = ask_for_age()
        self.assertEqual(age, 16)
        self.assertTrue(age < 17, "User is under 17. No R rated movies allowed.")

    # Test for if user did not input anything
    @patch('tkinter.simpledialog.askinteger', return_value=None)
    def test_no_input(self, mock_askinteger):
        age = ask_for_age()
        self.assertIsNone(age, "No age provided.")

    # Test for if user input 120, the maximum age
    @patch('tkinter.simpledialog.askinteger', return_value=120)
    def test_maximum_age(self, mock_askinteger):
        age = ask_for_age()
        self.assertEqual(age, 120)
        self.assertTrue(age >= 17, "User is an adult.")
    
    # Test for if user input 0, the minimum age
    @patch('tkinter.simpledialog.askinteger', return_value=0)
    def test_maximum_age(self, mock_askinteger):
        age = ask_for_age()
        self.assertEqual(age, 0)
        self.assertTrue(age < 17, "User is under 17. No R rated movies allowed.")

if __name__ == "__main__":
    if unittest.main(exit=False).result.wasSuccessful():
        # If unit tests pass, or if you simply want to run the manual part:
        user_age = ask_for_age()
        if user_age < 17:
                print(f"User is under 17. No R rated movies allowed.")
        else:
                print(f"User is an adult.")
