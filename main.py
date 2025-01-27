import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from surprise import SVD, Dataset, Reader
from flask import Flask, request, jsonify

# Load and preprocess dataset
def preprocess_data(file_path):
    movies_df = pd.read_csv(file_path)

    # One-Hot Encode Genres
    mlb = MultiLabelBinarizer()
    genre_matrix = pd.DataFrame(mlb.fit_transform(movies_df['Genres'].apply(lambda x: x.split(', '))),
                                columns=mlb.classes_,
                                index=movies_df.index)
    
    movies_df = pd.concat([movies_df, genre_matrix], axis=1)

    # Normalize Ratings
    scaler = MinMaxScaler()
    movies_df['Normalized_Rating'] = scaler.fit_transform(movies_df[['Rating']])

    return movies_df

# Content-Based Recommendation
def content_based_recommendation(movie_title, movies_df, top_n=5):
    features = movies_df.iloc[:, movies_df.columns.get_loc('Action'):].values
    similarity_matrix = cosine_similarity(features)

    movie_index = movies_df[movies_df['Title'] == movie_title].index[0]
    similarities = similarity_matrix[movie_index]
    recommended_indices = similarities.argsort()[-top_n-1:-1][::-1]

    return movies_df.iloc[recommended_indices][['Title', 'Genres', 'Rating']]

# Collaborative Filtering Setup
def train_collaborative_filtering(movies_df):
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(movies_df[['User', 'Title', 'Rating']], reader)
    trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)

    return algo

def collaborative_recommendation(user_id, algo, movies_df, top_n=5):
    user_movies = movies_df[movies_df['User'] == user_id]['Title'].tolist()
    all_movies = movies_df['Title'].unique()

    predictions = [
        (movie, algo.predict(user_id, movie).est)
        for movie in all_movies if movie not in user_movies
    ]
    
    top_recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]
    
    return [{'Title': movie, 'Predicted_Rating': rating} for movie, rating in top_recommendations]

# Hybrid Recommendation
def hybrid_recommendation(user_id, movie_title, algo, movies_df, top_n=5):
    content_recs = content_based_recommendation(movie_title, movies_df, top_n)
    collaborative_recs = collaborative_recommendation(user_id, algo, movies_df, top_n)

    hybrid_recs = pd.merge(
        pd.DataFrame(content_recs),
        pd.DataFrame(collaborative_recs),
        on='Title',
        how='outer'
    ).fillna(0)

    hybrid_recs['Hybrid_Score'] = hybrid_recs['Rating'] + hybrid_recs['Predicted_Rating']
    hybrid_recs = hybrid_recs.sort_values(by='Hybrid_Score', ascending=False)

    return hybrid_recs[['Title', 'Hybrid_Score']].head(top_n).to_dict(orient='records')

# Flask API
app = Flask(__name__)

if __name__ == "__main__":
    file_path = 'Movies.csv'
    movies_df = preprocess_data(file_path)
    print(movies_df.head())

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_id = data['user_id']
    movie_title = data['movie_title']

    recommendations = hybrid_recommendation(user_id, movie_title, algo, movies_df)
    return jsonify(recommendations)

if __name__ == '__main__':
    # Load dataset
    movies_df = preprocess_data('movies.csv')

    # Train collaborative filtering model
    algo = train_collaborative_filtering(movies_df)

    # Run the API
    app.run(debug=True)
