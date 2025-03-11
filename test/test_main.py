import pytest
import pandas as pd
from io import StringIO
from main import print_random_movie

# Mock CSV data for testing
MOCK_CSV_DATA = """Title,Rating
Inception,8.8
The Dark Knight,9.0
Interstellar,8.6
The Matrix,8.7
Fight Club,8.8
"""

# Helper function to mock reading CSV data
@pytest.fixture
def mock_csv(tmp_path):
    csv_file = tmp_path / "IMDB-Movie-Data.csv"
    csv_file.write_text(MOCK_CSV_DATA)
    return csv_file

def test_print_random_movie(capsys, mock_csv):
    # Run the function with mocked data
    print_random_movie(str(mock_csv))

    # Capture the printed output
    captured = capsys.readouterr()

    # Check if the output matches expected format
    assert "Random Movie Pick:" in captured.out
    assert "Rating:" in captured.out

    # Ensure the chosen movie is from the mock data
    movies_df = pd.read_csv(StringIO(MOCK_CSV_DATA))
    valid_titles = movies_df['Title'].tolist()
    valid_ratings = movies_df['Rating'].astype(str).tolist()

    # Extract title and rating from captured output
    movie_line, rating_line = captured.out.strip().split('\n')
    picked_movie = movie_line.replace("Random Movie Pick: ", "").strip()
    picked_rating = rating_line.replace("Rating: ", "").strip()

    assert picked_movie in valid_titles
    assert picked_rating in valid_ratings
