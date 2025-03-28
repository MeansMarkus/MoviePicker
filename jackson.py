import unittest
import tkinter as tk
from tkinter import simpledialog

# This method creates a pop up
def ask_for_age():
    # Creates a window pop up
    root = tk.Tk()
    root.withdraw()

    # Asks for age of the user
    age = simpledialog.askinteger("Movie Picker", "What is your age?", parent=root, minvalue=0, maxvalue=120)

    # Clean up
    root.destroy()
    return age

# Store user input in variable
user_age = ask_for_age()

if user_age < 18:
    print(f"User is a minor.")

else:
    print(f"User is an adult.")