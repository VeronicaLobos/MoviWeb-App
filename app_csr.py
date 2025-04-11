"""
*** Movie API ***
========================
This is a simple Flask web application that provides an API for managing
a movie database. The application allows users to add, update, and delete
movies, as well as manage user accounts. The application uses SQLAlchemy
to interact with a SQLite database and OMDB API to fetch movie data.

This program is a learning project for the Software Engineering
Bootcamp at MasterSchool. It showcases what I have learned
about Python programming, API and web development.
A step-by-step guide is included to help you understand how the
code has been implemented.

Author: https://github.com/VeronicaLobos
Date: 2025-April-11
Version: 1.0
License: Non-commercial use only
=========================

App Key Features:
 - REST architecture for the API, allowing for easy
    integration with other applications and services.
 - The API is built using Flask and SQLAlchemy, and it uses
    SQLite as the database.
 - Endpoints for adding, updating, and deleting movies, adding
    users, adding user ratings, and retrieving movie details
    and user ratings.
 - Input validation in every endpoint to ensure that the data
    provided by the user is valid and complete.
 - Error handling to return appropriate error messages
    when something goes wrong.
 - The API also fetches movie data from the OMDb API using the
    omdb_data_fetcher module (requires an API key).
 - JSON format for data exchange, making it easy to
    integrate with other applications and services (CSR).
 - DAL (Data Access Layer) is implemented using SQLAlchemy ORM
    with SQLite, through the DataManagerSQLite class, for
    managing database operations.
 - OOP (Object-Oriented Programming) is used to define the
    User and Movie classes, which represent the database tables.
 - The app is designed to be modular and easy to extend
    with additional features in the future.
"""
import os
import logging
import webbrowser
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from data_models import db, User, Movie
from datamanager.data_manager_sqlite import DataManagerSQLite
from omdb_data_fetcher import get_new_movie_data as data_fetcher

# [Step 1] Initialize the Flask application
# and SQLAlchemy database connection:
# - Initialize and configure the Flask application.............[√]
# - Create the database path...................................[√]
# - Set the SQLAlchemy database URI............................[√]
# - Initialize the SQLAlchemy instance with the Flask app......[√]
# - Initialize the DataManagerSQLite instance by passing
# the app and database.........................................[√]
# - Create the database and tables if they don't exist.........[√]

app = Flask(__name__)
CORS(app)
limiter = Limiter(app=app, key_func=get_remote_address)
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='my_log_file_csr.log')

database_path = os.path.join(os.path.dirname(__file__),
                                'data','movieapi.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = \
                                f'sqlite:///{database_path}'

db.init_app(app)
data_manager = DataManagerSQLite(app, db)

with app.app_context():
    if not os.path.exists(database_path):
        db.create_all()
        if db.session.query(User).count() == 0:
            db.create_all()
        if db.session.query(Movie).count() == 0:
            db.create_all()

# [Step 2] Define the API routes and their corresponding
# functions to handle requests:
# - Define the home route that returns a welcome message
#   and a list of all movies in the database.................[√]
# - Define the route to list all users in the database.......[√]
# - Define the route to list all movies associated with a
#   given user, with the user's ratings, and the username....[√]
# - Define the route to add a new user to the database.......[√]
# - Define the route to add a new movie to the user's
#   list of favorite movies..................................[√]
# - Define the route to update the rating of a specific
#   movie in the user's favorite movies list.................[√]
# - Define the route to update the details of a specific
#   movie in the user's favorite movies list.................[√]
# - Define the route to delete a movie from the user's
#   favorite movies list.....................................[√]
# - Define the route to display the details of a specific
#   movie....................................................[√]

## Utility function to validate movie data
def _validate_movie_data(movie_to_update, current_movie):
    """
    Validates the movie data to be updated.
    It checks the format of the data and updates
    the movie object with the new data.

    Parameters:
    :param movie_to_update: A dictionary containing the movie data
    :param current_movie: The current movie object to be updated

    Returns:
        Movie object with updated data or,
        error message if the data is invalid.
    """
    validation_rules = {
        'movie_name': (str, "Invalid movie name format"),
        'director': (str, "Invalid director format"),
        'year': (int, "Invalid year format",
                 lambda y: 1878 < y < 2031 and len(str(y)) == 4),
        'genre': (str, "Invalid genre format"),
        'poster_url': (str, "Invalid poster URL format")
    }

    for attribute, (expected_type, error_message, *conditions) \
            in validation_rules.items():
        if attribute in movie_to_update:
            new_value = movie_to_update[attribute]
            try:
                if not isinstance(new_value, expected_type):
                    return jsonify(error_message=error_message), 400
                if conditions:
                    if not all(condition(new_value) for condition in conditions):
                        return jsonify(error_message=error_message), 400
                # Update the movie attribute
                setattr(current_movie, attribute, new_value)
            except (ValueError, TypeError):
                return jsonify(message=f"Invalid format for '{attribute}'. "
                                f"Expected {expected_type.__name__}."), 400
        else:
            # If the attribute is not in the request, skip it
            continue

    return current_movie


@app.route('/home')
@limiter.limit("10/minute")
def home():
    """
    Returns a welcome message and a list of all
    movies in the database.
    If no movies are found, it returns a message
    indicating that no movies were found.
    """
    message = "Welcome to the Movie Web App!"

    movies = data_manager.get_all_movies()

    if movies:
        return jsonify(message=message,
                   movies=[{
                       'movie_id': movie.movie_id,
                       'movie_name': movie.movie_name,
                       'director': movie.director,
                       'year': movie.year,
                       'genre': movie.genre,
                       'poster_url': movie.poster_url
                   } for movie in movies]), 200

    message = "No movies found in the database."
    return jsonify(message=message), 404


@app.route('/users')
@limiter.limit("10/minute")
def list_all_users():
    """
    Returns a list of all users in the database,
    or a message indicating that no users were found.
    """
    user_list = data_manager.get_all_users()

    if user_list:
        return jsonify(
            user_list=[{
                'user_id': user.user_id,
                'user_name': user.user_name,
                'avatar_url': user.avatar_url
            } for user in user_list]), 200

    message = "No users found in the database."
    return jsonify(
        message=message,
    ), 404


@app.route('/users/<int:user_id>')
@limiter.limit("10/minute")
def list_user_movies(user_id):
    """
    Returns a list of all movies associated with a given user,
    with the user's ratings, and the user's name.
    If the user is not found, it returns a message
    indicating that the user was not found.
    If the user has no movies, it returns a message
    indicating that no movies were found for that user.
    """
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name(user_id)

    if user_name is None:
        message = f"Currently there is no user with ID {user_id}."
        return jsonify(message=message), 404

    if user_movies:
        # Extract the movie (Movie) and their ratings (int)
        user_movies = [(movie[0], movie[1]) for movie in user_movies]
        return jsonify(user_name=user_name,
            user_movies=[{
                'movie_id': movie[0].movie_id,
                'movie_name': movie[0].movie_name,
                'director': movie[0].director,
                'year': movie[0].year,
                'genre': movie[0].genre,
                'poster_url': movie[0].poster_url,
                'rating': movie[1]
            } for movie in user_movies]), 200

    message = f"User {user_name} has no movies."
    return jsonify(message=message), 404


@app.route('/add_user', methods=['GET', 'POST'])
@limiter.limit("1/minute")
def add_user():
    """
    Adds a new user to the database.

    * If a GET request is made, it returns a message
    indicating the required data to add a user.

    * If a POST request is made:
    - It retrieves the user data from the request.
    - It checks if the user data is valid (user_name and avatar_url).
    - It creates a new User object and adds it to the database.
    - If the user is added successfully, it returns a success message.
    - If the user is not added, it returns an error message.
    """
    if request.method == 'POST':
        new_user = request.get_json()
        if (not new_user or 'user_name' not in new_user
            or 'avatar_url' not in new_user):
            return jsonify({"error": "Invalid user data"}), 400

        user = User(user_name=new_user['user_name'],
                    avatar_url=new_user['avatar_url'])
        data_manager.add_user(user)

        if not user.user_id:
            error_message = "User not added or already in database."
            return jsonify({"error": error_message}), 500

        return jsonify(message="User added successfully!"), 201

    # If the method is 'GET'
    message = "Please, provide the following data: " \
              "user_name and avatar_url in JSON format."
    user_name = "A string or number (required)"
    avatar_url = "A string URL (optional)"
    return jsonify(message=message,
                   user_name=user_name,
                   avatar_url=avatar_url), 200


@app.route('/users/<int:user_id>/add_movie',
                         methods=['GET', 'POST'])
@limiter.limit("1/minute")
def add_movie(user_id):
    """
    Adds a new movie to the user's list of favorite movies.

    * If a GET request is made, it returns a message
    indicating the required data to add a movie.

    * If a POST request is made:
    - It retrieves the user ID from the URL.
    - It retrieves the movie name and rating from the request.
    - It checks if the movie data is valid (movie_name and
      rating).
    - It fetches the movie data from the OMDB API using the
      data_fetcher function.
    - If the movie is found, it creates a new Movie object
      and adds it to the database.
    - If the movie is not found or already exists, it returns
      an error message.
    """
    if request.method == 'POST':
        new_movie = request.get_json()
        print(new_movie)
        if (not new_movie
            or not isinstance(new_movie['movie_name'], str)
            or not isinstance(new_movie['rating'], (float, int))
            or 10.0 < new_movie['rating'] < 0.0
            or 'movie_name' not in new_movie
            or 'rating' not in new_movie):
            return jsonify({"error": "Invalid movie data"}), 400

        movie_name, rating = new_movie['movie_name'], new_movie['rating']
        new_movie_obj = data_fetcher(movie_name)

        # If new_movie_obj is None, it means the movie was not found, or
        # there was an error fetching the data, or no internet connection
        if new_movie_obj is None:
            message = f"Movie {new_movie.movie_name} not found."
            return jsonify({"error": message}), 404

        # If the movie was found, a Movie object is returned
        # and can be added to the database
        new_movie_exists = data_manager.add_movie(new_movie_obj,
                                        user_id, rating)

        if new_movie_exists:
            message = (f"Movie {new_movie_obj.movie_name} added successfully"
                       f" with rating {rating}!")
            return jsonify(message=message), 201

        message = f"Movie {new_movie_obj.movie_name} already exists."
        return jsonify({"error": message}), 400

    # If the method is 'GET'
    message = "Please, provide the following data: " \
              "movie_name and rating in JSON format."
    movie_name = "A string (required)"
    rating = "A float between 0.0 and 10.0 (required)"
    return jsonify(message=message,
                   movie_name=movie_name,
                   rating=rating), 200


@app.route('/users/<int:user_id>/update_rating/<int:movie_id>',
                                            methods=['GET', 'POST'])
@limiter.limit("1/minute")
def update_rating(user_id, movie_id):
    """
    Updates the rating of a specific movie in the user's
    favorite movies list.

    * If a GET request is made, it returns a message
    indicating the required data to add a movie.

    * If a POST request is made:
    - It retrieves the user ID and movie ID from the URL.
    - It retrieves the rating from the request.
    - It checks if the rating is valid (a float between
      0.0 and 10.0).
    - It fetches the movie data from the database using
      the data_manager instance.
    - If the movie is found, it updates the rating in the
      database and returns a success message.
    - If the movie is not found or the rating is invalid,
      it returns an error message.
    """
    if request.method == "POST":
        rating = request.get_json()

        if (not rating or 'rating' not in rating
        or not isinstance(rating['rating'], (float, int))
        or rating['rating'] < 0.0 or rating['rating'] > 10.0):
            return jsonify({"error": "Invalid rating data"}), 400

        movie = data_manager.get_movie(movie_id)

        updated_movie = data_manager.update_rating(user_id,
                            movie_id, rating['rating'])

        if updated_movie:
            message = f"Movie {movie.movie_name} updated successfully!"
            return jsonify(message=message), 200

        message = f"Movie {movie.movie_name} not found."
        return jsonify({"error": message}), 404

    # If the method is 'GET'
    message = "Please, provide the following data: " \
              "rating in JSON format."
    rating = "A float between 0.0 and 10.0"
    return jsonify(message=message, rating=rating), 200


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
                                            methods=['GET', 'POST'])
@limiter.limit("1/minute")
def update_movie(user_id, movie_id):
    """
    This route allows a user to update the details of a
    specific movie in their favorite movies list.
    Only registered users can update movies in the database.

    * If a GET request is made, it returns a message
    indicating the required data to update a movie.
    All fields are optional, and the user can update
    any combination of them or none at all.

    * If a POST request is made:
    - It retrieves the user ID and movie ID from the URL.
    - It checks that the user is registered,
        and returns an error message if not.
    - It retrieves the movie details currently in the database,
        and checks if the movie exists, otherwise
        returns an error message.
    - It retrieves the movie details from the request.
    - It checks if the movie data is valid (movie_name,
        director, year, genre, poster_url), if the
        data is not valid, it returns an error message.
        If the data is valid, it updates the movie object
        with the new attributes.
    - It updates the movie details in the database, and
        returns a success message (yay!).
    """
    if request.method == "POST":
        user = data_manager.get_user_name(user_id)
        if user is None:
            message = f"User with ID {user_id} not found."
            return jsonify(message=message), 404

        current_movie = data_manager.get_movie(movie_id)
        if current_movie is None:
            message = f"Movie with ID {movie_id} not found."
            return jsonify(message=message), 404

        movie_to_update = request.get_json()

        if not movie_to_update:
            message = "No movie data to update"
            return jsonify(message=message), 400

        # Validate the movie data
        updated_movie = _validate_movie_data(movie_to_update,
                                              current_movie)
        if isinstance(updated_movie, tuple):
            return updated_movie

        # Finally, update the movie in the database
        updated_movie_name = data_manager.update_movie(updated_movie)

        if updated_movie_name:
            message = (f"Movie {updated_movie_name} updated "
                       f"successfully!")
            return jsonify(message=message), 200

    ## If the method is 'GET'
    return jsonify(
        message="Please, provide the following data to update"
                " a movie: ",
        movie_name="A string (optional)",
        director="A string (optional)",
        year="An integer with length 4 and 1878 < value < 2031"
                " (optional)",
        genre="A string (optional)",
        poster_url="A string URL (optional)"), 200


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>',
                                                  methods=['POST'])
@limiter.limit("1/minute")
def delete_movie(user_id, movie_id):
    """
    This route allows a user to delete a specific movie
    from their favorite movies list.
    Only registered users can delete movies from the database.

    * When a POST request is made:
    - It retrieves the user ID and movie ID from the URL.
    - It checks that the user is registered, otherwise
      returns an error message.
    - It checks if the movie exists in the database,
      otherwise returns an error message.
    - Calls the delete_movie method from the data_manager
      instance to delete the movie from the database.
    - If the movie is deleted successfully, it returns
      a success message.

    Note: If no other user has the same movie in their list,
    the movie will be deleted from the database.
    """
    if request.method == 'POST':
        user = data_manager.get_user_name(user_id)
        if user is None:
            message = f"User with ID {user_id} not found."
            return jsonify(message=message), 404

        current_movie = data_manager.get_movie(movie_id)
        if current_movie is None:
            message = f"Movie with ID {movie_id} not found."
            return jsonify(message=message), 404

        deleted_movie = data_manager.delete_movie(user_id, movie_id)
        if deleted_movie:
            message = (f"Movie {deleted_movie.movie_name} "
                       f"deleted successfully!")
            return jsonify(message=message), 200


@app.route('/movie/<movie_id>')
@limiter.limit("10/minute")
def movie_details(movie_id):
    """
    Returns the details of a specific movie,
    or a message indicating that the movie was not found.
    """
    try:
        movie = data_manager.get_movie(movie_id)
        if movie:
            return jsonify(movie_id=movie.movie_id,
                           movie_name=movie.movie_name,
                           director=movie.director,
                           year=movie.year,
                           genre=movie.genre,
                           poster_url=movie.poster_url,
                           plot=movie.plot), 200
    except Exception as e:
        app.logger.error(f"Error fetching movie: {e}")
        return jsonify(message="Error fetching movie data."), 500

    message = f"Movie with ID {movie_id} not found."
    return jsonify(message=message), 404


@app.errorhandler(404)
def not_found(error):
    """
    Returns a 404 error message for any invalid URL.
    """
    return jsonify(message="This URL is not valid, error 404."), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Returns a 500 error message for any server errors.
    """
    app.logger.warning(f"Internal server error: {error}")
    return jsonify(message="Internal server error, error 500."), 500


# [Step 3] Define the main function to run the Flask application

if __name__ == '__main__':
    # Example URLs to test the API:
    URL_HOME = 'http://127.0.0.1:5002/home'
    URL_USERS = 'http://127.0.0.1:5002/users'
    URL_USER_1 = 'http://127.0.0.1:5002/users/1'
    webbrowser.open_new(URL_HOME)
    app.run(port=5002, debug=True)
