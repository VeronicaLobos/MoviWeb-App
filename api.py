"""
*** Movie API ***
========================

"""
import os
import webbrowser
from flask import Flask, request, jsonify
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

@app.route('/home')
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

    message = "Please, provide the following data: " \
              "user_name and avatar_url in JSON format."
    user_name = "A string (required)"
    avatar_url = "A string URL (optional)"
    return jsonify(message=message,
                   user_name=user_name,
                   avatar_url=avatar_url), 200


@app.route('/users/<int:user_id>/add_movie',
                         methods=['GET', 'POST'])
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
        if (not new_movie or ('movie_name' not in new_movie
            and 'rating' not in new_movie)):
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

    message = "Please, provide the following data: " \
              "movie_name and rating in JSON format."
    movie_name = "A string (required)"
    rating = "A float between 0.0 and 10.0 (required)"
    return jsonify(message=message,
                   movie_name=movie_name,
                   rating=rating), 200


@app.route('/users/<int:user_id>/update_rating/<int:movie_id>', ## TODO!!!!!!
                                            methods=['GET', 'POST'])
def update_rating(user_id, movie_id):
    """
    This route will display a form allowing for the updating
    of details of a specific movie in a user’s list.

    * If a GET request is made, it renders the update_rating.html
    template with a form to update the rating of a movie.

    * If a POST request is made:
    - It retrieves the updated rating from the request form.
    - Calls the update_rating method of the DataManagerSQLite
      instance to update the rating of the movie in the database.

    Returns:
        - It renders the redirect.html template with a
        message informing the user with the resulting operation,
        either the movie was updated successfully or not found.
    """
    if request.method == "POST":
        rating = request.form.get('rating')

        movie = data_manager.get_movie(movie_id)

        updated_movie = data_manager.update_rating(user_id,
                            movie_id, rating)

        if updated_movie:
            status = "Movie updated"
            message = f"Movie {movie.movie_name} updated successfully!"
            return render_template('redirect.html',
                                   status=status,
                                   message=message,
                                   user_id=user_id,
                                   movie_id=movie_id), 200

        status = "Movie not found"
        message = f"Movie {movie.movie_name} not found."
        return render_template('redirect.html',
                                   status=status,
                                   message=message,
                                   user_id=user_id,
                                   movie_id=movie_id), 404

    return render_template('update_rating.html',
                            user_id=user_id, movie_id=movie_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
                                            methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    This route will display a form allowing for the updating
    of details of a specific movie. Update requires a user id,
    this way only registered users can update the movies in
    the database (it also allows tracking who made the changes).

    * If a GET request is made, it renders the update_movie.html
    template with a form to update the movie details.

    * If a POST request is made:
    - It retrieves the current movie object from the database
      (with the given movie_id parameter in the URL).
    - If the movie exists in the database: it retrieves the
      updated movie details from the request form (only the
      fields that have been filled out by the user will be
      updated), and updates the movie object with the new values.
    - Calls the update_movie method of the DataManagerSQLite
      instance to update the movie in the database.

    Returns:
        It renders the redirect.html template with a
        message informing the user with the resulting operation,
        either the movie was updated successfully or not found.
    """
    if request.method == "POST":
        movie_to_update = data_manager.get_movie(movie_id)

        if movie_to_update:
            if 'movie_name' in request.form and request.form['movie_name']:
                movie_to_update.movie_name = request.form['movie_name']
            if 'director' in request.form and request.form['director']:
                movie_to_update.director = request.form['director']
            if 'year' in request.form and request.form['year']:
                movie_to_update.year = request.form['year']
            if 'genre' in request.form and request.form['genre']:
                movie_to_update.genre = request.form['genre']
            if 'poster_url' in request.form and request.form['poster_url']:
                movie_to_update.poster_url = request.form['poster_url']

        updated_movie_name = data_manager.update_movie(movie_to_update)

        if updated_movie_name:
            status = "Movie updated"
            message = f"Movie {updated_movie_name} updated successfully!"
            return render_template('redirect.html',
                                   status=status,
                                   message=message,
                                   user_id=user_id,
                                   movie_id=movie_id), 200

        status = "Movie not found"
        message = f"Movie with ID {movie_to_update.movie_name} not found."
        return render_template('redirect.html',
                                   status=status,
                                   message=message,
                                   user_id=user_id,
                                   movie_id=movie_id), 404

    ## If the method is 'GET'
    movie = data_manager.get_movie(movie_id)
    return render_template('update_movie.html',
                            user_id=user_id,
                            movie_id=movie_id,
                            movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Upon visiting this route, a specific movie will be removed
    from a user’s favorite movie list.

    * Only registered users can delete movies from the database
    """
    # Call the delete_movie method to delete the movie from the database
    # should return the deleted movie name
    deleted_movie = data_manager.delete_movie(user_id, movie_id)
    if deleted_movie:
        status = "Movie deleted"
        message = f"Movie {deleted_movie.movie_name} deleted successfully!"
        return render_template('redirect.html',
                               status=status,
                               message=message,
                               user_id=user_id,
                               movie_id=movie_id), 200

    status = "Movie not found"
    message = f"Movie with ID {movie_id} not found."
    return render_template('redirect.html',
                               status=status,
                               message=message,
                               user_id=user_id,
                               movie_id=movie_id), 404


@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    """
    Returns the details of a specific movie.
    """
    movie = data_manager.get_movie(movie_id)
    if movie:
        return render_template('movie_info.html',
                               movie=movie), 200

    message = "Movie not found."
    return render_template('movie_info.html',
                               message=message), 404


if __name__ == '__main__':
    # Example URLs to test the API:
    URL_HOME = 'http://127.0.0.1:5002/home'
    URL_USERS = 'http://127.0.0.1:5002/users'
    URL_USER_1 = 'http://127.0.0.1:5002/users/1'
    webbrowser.open_new(URL_HOME)
    app.run(port=5002, debug=True)
