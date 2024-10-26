from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample movie data
movies = [
    {"id": 1, "title": "Inception", "genre": "Sci-Fi", "rating": 8.8},
    {"id": 2, "title": "The Godfather", "genre": "Crime", "rating": 9.2},
    {"id": 3, "title": "The Dark Knight", "genre": "Action", "rating": 9.0}
]

# Route to get all movies
@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

# Route to get movies by genre
@app.route('/api/movies/genre/<string:genre>', methods=['GET'])
def get_movies_by_genre(genre):
    genre_movies = [movie for movie in movies if movie["genre"].lower() == genre.lower()]
    return jsonify({"movies": genre_movies, "count": len(genre_movies)})

# Route to get movie recommendations based on rating threshold
@app.route('/api/movies/recommend', methods=['GET'])
def recommend_movies():
    min_rating = float(request.args.get('min_rating', 8.0))
    recommended_movies = [movie for movie in movies if movie["rating"] >= min_rating]
    return jsonify({"recommended_movies": recommended_movies})

# Route to add a new movie
@app.route('/api/movies', methods=['POST'])
def add_movie():
    new_movie = request.get_json()
    new_movie["id"] = max(movie["id"] for movie in movies) + 1 if movies else 1
    movies.append(new_movie)
    return jsonify(new_movie), 201

# Route to update a movie by ID
@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if movie:
        update_data = request.get_json()
        movie.update(update_data)
        return jsonify(movie)
    else:
        return jsonify({"message": "Movie not found"}), 404

# Route to delete a movie by ID
@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    global movies
    movies = [movie for movie in movies if movie["id"] != movie_id]
    return jsonify({"message": "Movie deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
