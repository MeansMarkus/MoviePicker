# Movie Recommendation System

This project implements a hybrid movie recommendation system using both content-based filtering and collaborative filtering techniques. It takes input from users about movies they have watched and provides movie recommendations based on their preferences. The recommendation engine uses features such as genres, ratings, and actors to suggest movies that the users are likely to enjoy. 

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The Movie Recommendation System provides movie suggestions using two main approaches:
1. **Content-Based Filtering**: This method suggests movies similar to the ones the user has rated highly, using metadata such as genres, actors, and ratings.
2. **Collaborative Filtering**: This method recommends movies based on the preferences of similar users (user-item interactions).
3. **Hybrid Approach**: A combination of both content-based and collaborative filtering to provide more accurate recommendations.

The system can recommend movies that are enjoyable for a group of users based on their collective movie preferences, including genre, actors, and ratings.

---

## Technologies Used

- **Python**
- **Flask**: For creating the API that serves recommendations.
- **Pandas**: For data manipulation and preprocessing.
- **Scikit-learn**: For implementing content-based filtering using cosine similarity.
- **Surprise**: For collaborative filtering with the SVD algorithm.
- **MinMaxScaler**: For normalizing ratings.
- **MultiLabelBinarizer**: For encoding movie genres.

---

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   ```

2. **Install Dependencies**  
   Install the necessary Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Dataset**  
   Place your `Movies.csv` file in the project directory. The CSV file should contain at least the following columns:
   - `User`: User identifier
   - `Title`: Movie title
   - `Genres`: Comma-separated list of genres
   - `Rating`: Rating provided by the user

4. **Run the Flask API**  
   Start the Flask API by running the following command:
   ```bash
   python app.py
   ```

   The API will be accessible at `http://127.0.0.1:5000/`.

---

## Usage

To get movie recommendations, send a **POST request** to the `/recommend` endpoint with the following JSON body:

```json
{
  "user_id": 1,
  "movie_title": "The Matrix"
}
```

- `user_id`: The ID of the user requesting recommendations.
- `movie_title`: The title of the movie that the user has watched or is interested in.

### Example Response:
```json
[
  {
    "Title": "Inception",
    "Hybrid_Score": 8.7
  },
  {
    "Title": "Interstellar",
    "Hybrid_Score": 8.5
  }
]
```

The response will contain a list of recommended movies sorted by the hybrid score, combining content-based and collaborative filtering.

---

## API Documentation

### Endpoint: `/recommend`

- **Method**: POST
- **Request Body**:
  - `user_id`: Integer (User ID)
  - `movie_title`: String (Movie title the user has watched or likes)
  
- **Response**:
  A JSON array of recommended movies, each containing:
  - `Title`: The movie title.
  - `Hybrid_Score`: The combined score based on content and collaborative filtering.

---

## Contributing

Contributions: Only Group H members

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes
4. Push to your forked repository
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
