import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load and preprocess dataset
def preprocess_data(file_path):
    movies_df = pd.read_csv(file_path)

    # Fill missing values
    movies_df.fillna('', inplace=True)

    # Normalize numerical features
    scaler = MinMaxScaler()
    numerical_features = ['Rating', 'Votes', 'Revenue (Millions)', 'Metascore', 'Runtime (Minutes)']

    for feature in numerical_features:
        if movies_df[feature].dtype != 'object':
            movies_df[feature] = scaler.fit_transform(movies_df[[feature]].fillna(0))

    # Create "soup" combining important features as text
    movies_df['soup'] = movies_df.apply(lambda x: f"{x['Genre']} {x['Description']} {x['Director']} {x['Actors']} {x['Year']} {x['Rating']} {x['Votes']} {x['Revenue (Millions)']} {x['Metascore']} {x['Runtime (Minutes)']}", axis=1)

    return movies_df
def recommend_movies(user_movie_titles, movies_df, top_n=5):
    # Vectorize the "soup" using TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['soup'])

    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get indices of the user-selected movies
    movie_indices = movies_df[movies_df['Title'].isin(user_movie_titles)].index.tolist()

    # Sum the similarity scores of all user-selected movies
    similarity_scores = similarity_matrix[movie_indices].sum(axis=0)

    # Get movie indices sorted by similarity scores (descending), excluding user-selected movies
    similar_movies_indices = similarity_scores.argsort()[::-1]

    # Remove the movies the user already provided
    similar_movies_indices = [i for i in similar_movies_indices if i not in movie_indices]

    # Get top N recommended movies
    recommended_movies = movies_df.iloc[similar_movies_indices[:top_n]][['Title', 'Genre', 'Rating']]

    return recommended_movies

if __name__ == "__main__":
    file_path = 'IMDB-Movie-Data.csv'
    movies_df = preprocess_data(file_path)

    user_input_movies = ["The Shawshank Redemption", "The Godfather"]
    recommendations = recommend_movies(user_input_movies, movies_df)

    print("Recommended Movies:")
    print(recommendations)
