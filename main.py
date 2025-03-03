import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


def preprocess_data(file_path):
    movies_df = pd.read_csv(file_path)

    # Fill missing values
    movies_df.fillna('', inplace=True)

    # Convert numerical columns to numeric type (handle non-numeric)
    numerical_features = ['Rating', 'Votes', 'Revenue (Millions)', 'Metascore',
                          'Runtime (Minutes)']
    scaler = MinMaxScaler()

    for feature in numerical_features:
        movies_df[feature] = pd.to_numeric(movies_df[feature], errors='coerce')
        movies_df[feature].fillna(movies_df[feature].median(), inplace=True)
        movies_df[feature] = scaler.fit_transform(movies_df[[feature]])

    # Combine features into a "soup"
    movies_df['soup'] = movies_df.apply(
    lambda x: ' '.join([
        str(x['Genre']), str(x['Description']), str(x['Director']), str(x['Actors']),
        str(x['Year']), str(x['Rating']), str(x['Votes']), str(x['Revenue (Millions)']),
        str(x['Metascore']), str(x['Runtime (Minutes)'])
    ])
, axis=1)


    # Standardize titles to lowercase for better matching
    movies_df['Title'] = movies_df['Title'].str.lower()

    return movies_df


def recommend_movies(user_movie_titles, movies_df, top_n=5):
    # Lowercase the user input for title matching
    user_movie_titles = [title.lower() for title in user_movie_titles]

    # Vectorize the "soup"
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['soup'])

    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get indices of user-selected movies
    movie_indices = movies_df[movies_df['Title'].isin(user_movie_titles)].index.tolist()

    if not movie_indices:
        print("No matching movies found. Please check the movie titles.")
        return pd.DataFrame()

    # Sum the similarity scores of all user-selected movies
    similarity_scores = similarity_matrix[movie_indices].sum(axis=0)

    # Get indices sorted by similarity
    similar_movies_indices = similarity_scores.argsort()[::-1]

    # Remove already selected movies
    similar_movies_indices = [i for i in similar_movies_indices if i not in movie_indices]

    # Get top N recommendations
    recommended_movies = movies_df.iloc[similar_movies_indices
    [:top_n]][['Title', 'Genre', 'Rating']]

    return recommended_movies


if __name__ == "__main__":
    file_path = 'IMDB-Movie-Data.csv'
    movies_df = preprocess_data(file_path)

    user_input_movies = ["The Shawshank Redemption", "The Godfather"]
    recommendations = recommend_movies(user_input_movies, movies_df)

    if not recommendations.empty:
        print("Recommended Movies:")
        print(recommendations)
