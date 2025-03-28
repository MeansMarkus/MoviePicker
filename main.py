import pandas as pd
import random
from movieFilter import print_random_movie_by_genre # -ian

def print_random_movie(file_path='IMDB-Movie-Data.csv'):
    
    # Load the CSV into a DataFrame
    movies_df = pd.read_csv(file_path)

    # Pick a random row
    random_index = random.randint(0, len(movies_df) - 1)
    
    # Get the title of the random movie
    random_movie = movies_df.iloc[random_index]['Title']

    # Print the result
    print(f"Random Movie Pick: {random_movie}")

    #get the rating of the random movie
    random_movie_rating = movies_df.iloc[random_index]['Rating']

    #print the rating
    print(f"Rating: {random_movie_rating}")

if __name__ == "__main__":
    #print_random_movie()
    print_random_movie_by_genre() # -ian