from flask import Flask, render_template, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load movie data once at startup
movies_df = pd.read_csv('IMDB-Movie-Data.csv')

@app.route('/')
def home():
    return render_template('index.html')  # Make sure 'index.html' is in a `/templates` folder

@app.route('/random-movie', methods=['GET'])
def get_random_movie():
    random_index = random.randint(0, len(movies_df) - 1)
    random_movie = movies_df.iloc[random_index]['Title']
    random_movie_rating = movies_df.iloc[random_index]['Rating']

    return jsonify({
        "movie": random_movie,
        "rating": random_movie_rating
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
