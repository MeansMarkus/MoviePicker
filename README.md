# Movie Recommendation System

This project implements a movie recommendation system using both content-based filtering and collaborative filtering techniques. It takes input from users about movies they have watched and provides movie recommendations based on their preferences. The recommendation engine uses features such as genres, ratings, and actors to suggest movies that the users are likely to enjoy. 

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

The system can recommend movies that are enjoyable for a group of users based on their collective movie preferences, including genre, actors, and ratings.

---

## Technologies Used

- **Python**: Language
- **Flask**: For creating the API that serves recommendations.
- **Pandas**: For data manipulation and preprocessing.
- **Scikit-learn**: For implementing content-based filtering using cosine similarity.
- **MinMaxScaler**: For normalizing ratings.

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
   Place your `IMDB-Movie_data.csv` file in the project directory. The CSV file should contain at least the following columns:
   - `User`: User identifier
   - `Title`: Movie title
   - `Genres`: Comma-separated list of genres
   - `Rating`: Rating provided by IMDB
   - `Actors`: Comma-separated list of actors
   - `Director`: Director of the movie
   - `Year`: Release year of the movie
   - `Description`: Brief description of the movie
   - `Votes`: Number of votes
   - `Metascore`: Metascore rating



4. **Run the Flask API**  
   Start the Flask API by running the following command:
   ```bash
   python app.py
   ```

   The API will be accessible at `http://127.0.0.1:5000/`.

---

## Usage

Modify the user_input_movies list in the script to include the movie titles you like.

Example 

user_input_movies = ["The Shawshank Redemption", "The Godfather"]

The program will output the top recommended movies based on the input.

Recommended Movies:
                      Title    Genre  Rating
34  The Dark Knight Rises  Action     8.4
48                Gladiator  Action     8.5
27         The Dark Knight  Action     9.0

---

## API Documentation




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
