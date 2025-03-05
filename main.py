import pandas as pd
import random

def print_random_movie(file_path='IMDB-Movie-Data.csv'):
    # Load the CSV into a DataFrame
    movies_df = pd.read_csv(file_path)

    # Pick a random row
    random_index = random.randint(0, len(movies_df) - 1)

    # Get the title of the random movie
    random_movie = movies_df.iloc[random_index]['Title']

    # Print the result
    print(f"Random Movie Pick: {random_movie}")

if __name__ == "__main__":
    print_random_movie()

