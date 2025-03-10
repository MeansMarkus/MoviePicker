from flask import Flask, jsonify, send_file
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

if __name__ == "__main__":
    app.run(debug=True)
