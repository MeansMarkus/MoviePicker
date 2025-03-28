import unittest
import tkinter as tk
from tkinter import simpledialog

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

# Store user input in variable
user_age = ask_for_age()


# Output
if user_age < 17:
    print(f"User is under 17. No R rated movies allowed.")

else:
    print(f"User is an adult.")