import pandas as pd
import random

def print_random_movie_by_genre(file_path='IMDB-Movie-Data.csv'):
    # Load the CSV into a DataFrame
    movies_df = pd.read_csv(file_path)
    
    #Action,Adventure,Comedy,Sci-Fi,Thiller,Fantasy,Biography,Drama,History,Romance,War,Crime.Musical,Western,Family,Horror,Mystery
    
    user_genre = input("Please enter your desired genre! ")
    #if (input != )

    # Pick a random row
    random_index = random.randint(0, len(movies_df) - 1)
    
    # Finds a random movie and sees if it matches the given input for the genre
    random_movie = movies_df.iloc[random_index]['Title']
    random_movie_genre = movies_df[movies_df['Title'] == random_movie]['Genre'].values[0]
    print("Genre:", random_movie_genre)
    
    # creates an array holding the genres of the specific movie
    genreArray = random_movie_genre.split(",")
    print(genreArray) - #testing to see what genres are in this
    
    # if the user's input genre is not one of the initial randomly generated movie's genres, enter this loop to find one until it does
    if user_genre not in genreArray:
        genreMatched = False
        while genreMatched == False:
            random_index = random.randint(0, len(movies_df) - 1)
            random_movie = movies_df.iloc[random_index]['Title']
            random_movie_genre = movies_df[movies_df['Title'] == random_movie]['Genre'].values[0]
            genreArray = random_movie_genre.split(",")
            for genre in genreArray:
                if genre.strip().lower() == user_genre.lower():
                    genreMatched = True
                    break

    #
    print(f"Random Movie Pick based off genre: {random_movie}")
    print("Genre:", random_movie_genre)
    
 