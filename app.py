from flask import Flask, jsonify, send_file, request
import pandas as pd
import random

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')  # Serves the front-end UI

@app.route('/get-random-movie')
def get_random_movie():
    movies_df = pd.read_csv('IMDB-Movie-Data.csv')
    random_index = random.randint(0, len(movies_df) - 1)
    random_movie = movies_df.iloc[random_index]['Title']
    random_movie_rating = movies_df.iloc[random_index]['Rating']

    return jsonify({
        'title': random_movie,
        'rating': random_movie_rating
    })

#Patrick's Code portion 
@app.route('/recommend-movie', methods=['POST'])
def recommend_movie():
    favorite_movies = request.json('favorite_movies', [])

    movies_df = pd.read_csv('IMDB-Movie-Data.csv')
    recommended_movies = movies_df[~movies_df['Title'].isin(favorite_movies)]

    if recommended_movies.empty:
        return jsonify({'error': 'No movies to recommend'}), 404
    
    random_index = random.randint(0, len(recommended_movies) - 1)
    random_movie = recommended_movies.iloc[random_index]['Title']
    random_movie_rating = recommended_movies.iloc[random_index]['Rating']

    return jsonify({
        'recommended_movie': random_movie,
        'rating': random_movie_rating
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))  # Railway uses dynamic ports
    app.run(host="0.0.0.0", port=port)

