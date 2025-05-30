"""
*** Movie Web App ***
========================

This is a Restful API for a Movie Web App that allows users to
manage a list with their favorite movies, as well as retrieve
movie details from the OMDb API and edit the movie information.

This program is a learning project for the Software Engineering
Bootcamp at MasterSchool. It showcases what I have learned
about Python programming, API and web development.
A step-by-step guide is included to help you understand how the
code has been implemented.

Author: https://github.com/VeronicaLobos
Date: 2025-April-11
Version: 1.0
License: Non-commercial use only
========================

App Key Features:
 - Restful API architecture with CRUD operations for managing
    movies and users.
 - The API is built using Flask and SQLAlchemy, and it uses
    SQLite as the database.
 - Endpoints for adding, updating, and deleting movies, adding
    users, and retrieving movie details.
 - Input validation in templates to ensure that the user
    provides valid data before submitting the form.
 - The API also fetches movie data from the OMDb API using the
    omdb_data_fetcher module (requires an API key).
 - SSR (Server-Side Rendering) is used to render HTML jinja2
    templates for the web application, and a stylesheet
    (style.css) with a responsive minimalist design is included.
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
from flask import Flask, request, render_template
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

app = Flask(__name__, static_folder='_static')
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='my_log_file_ssr.log')

database_path = os.path.join(os.path.dirname(__file__),
                                'data','moviewebapp.sqlite')
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


# [Step 2] Define the API endpoints:
# - 1. Define the home route ..................................[√]
#     · Fetches all movies from the db
# - 2. Define the route to list all users......................[√]
#     · Fetches all users and avatars from the db
# - 3. Define the route to list user movies....................[√]
#     · Fetches all movies associated with a user
# - 4. Define the route to add a user..........................[√]
#     · Adds a new user to the db
# - 5. Define the route to add a movie.........................[√]
#     · Adds a new movie to the db and to the user's list
# - 6. Define the route to update a movie......................[√]
#     · Updates a movie information in the db
# - 7. Define the route to delete a movie......................[√]
#     · Deletes a movie from the user's list,
#       and from the db if no other user has rated it
# - Extra. Define the route to get movie details...............[√]
#     · Fetches a movie's details from the db
# - Extra. Define the route to get about information...........[√]
#     · Shows information about the app
# - Extra. Define the route to handle errors...................[√]
#     · Handles 404 and 500 errors

@app.route('/')
def home():
    """
    Renders the home page of the application with a welcome
    message, buttons to navigate to different sections
    of the application, and all movie posters in the database
    displayed in a grid format with links to their details.
    """
    app.logger.info("Home page accessed")
    message = "Welcome to the Movie Web App!"

    movies = data_manager.get_all_movies()

    return render_template('home.html',
                           message=message,
                           movies=movies), 200


@app.route('/users')
def list_all_users():
    """
    Returns a render of the users template with a list of all
    users in the database, each linked to their respective
    movie lists.
    If no users are found, it returns a message.
    """
    app.logger.info("List of all users accessed")
    user_list = data_manager.get_all_users()

    if user_list:
        return render_template('users.html',
                               user_list=user_list), 200

    message = "No users found in the database."
    return render_template('users.html',
                               message=message), 404


@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    """
    Returns a list of all movies associated with a given user.
    Each movie is linked to its details page.
    Each movie has a button for:
    · updating the movie information
    · deleting the movie from the user's list

    - Queries the database for all movies associated with the
    user by calling the get_user_movies method of the
    DataManagerSQLite instance.
    - Queries the database for the user_name associated with
    the user_id.

    Returns a render of the user_movies.html template with
    the list of movies containing the movie name, the user_id
    and the user_name.
    If no movies are found for the user, it renders the template
    with a message indicating that no movies were found.
    """
    app.logger.info(f"List of movies for user {user_id} accessed")
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name(user_id)

    if user_movies:
        user_movies = [movie for movie in user_movies]
        return render_template('user_movies.html',
                               user_id=user_id,
                               user_movies=user_movies,
                               user_name=user_name), 200

    message = "No movies found for this user."
    return render_template('user_movies.html',
                               user_id=user_id,
                               message=message,
                               user_name=user_name), 404


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Adds a new user to the database.

    * If a GET request is made, it renders the add_user.html
    template with a form to add a new user.

    * If a POST request is made, it retrieves the user data
    from the request form, creates a new User object with it,
    and adds it to the database by calling the add_user method
    of the DataManagerSQLite instance.

    Returns a render of the add_user.html template with a success
    message, or a message indicating that the user already exists.
    """
    if request.method == 'POST':
        app.logger.info("POST request to add a new user")
        if 'avatar_url' in request.form and request.form['avatar_url']:
            avatar_url = request.form['avatar_url']

        else:
            # If no avatar_url is provided, use a default one
            avatar_url = ("https://gravatar.com/userimage/12498767/"
                "cf086b8eb3c9ffbc5147271157598803.jpeg?size=256")

        new_user_obj = User(
            user_name=request.form.get('user_name'),
            avatar_url=avatar_url
        )

        new_user_exists = data_manager.add_user(new_user_obj)

        if new_user_exists:
            message = f"User {new_user_obj.user_name} added successfully!"
            app.logger.info(message)
            return render_template('add_user.html', message=message), 201

        message = f"User {new_user_obj.user_name} already exists."
        return render_template('add_user.html', message=message), 400

    app.logger.info("GET request to add a new user")
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Adds a new movie to the database.

    * If a GET request is made, it renders the add_movie.html
     template with a form to add a new movie.
     - Only users with a user_id can add movies to the database.

    * If a POST request is made:
    - It retrieves the movie name associated to that id from the
      request form.
    - Calls data_fetcher to fetch the movie data from the OMDb API.
    - A Movie object is returned (if the movie is found in the API).
    - Calls the add_movie method of the DataManagerSQLite instance
      to add the movie to the database:
        - If the movie already exists, it will not be added again.
        - It checks if there is already a relationship
          with that user_id and movie_id in the UserMovies table.
        - If a relationship already exists, it will not be added
          again.

    Returns:
        If the movie is added successfully, it returns a render
        containing a message informing the user with the resulting
        operation.
        Note: by providing the user_id in the render_template,
        it allows the user to resubmit the form. This avoids
        the flask app from crashing when the route is not found.
    """
    if request.method == 'POST':
        app.logger.info("POST request to add a new movie by {user_id}")

        movie_name = request.form.get('movie_name')
        new_movie_obj = data_fetcher(movie_name)

        if new_movie_obj is None:
            message = f"Movie {movie_name} not found."
            return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 404

        new_movie_exists = data_manager.add_movie(new_movie_obj,
                                                  user_id)

        if new_movie_exists:
            message = f"Movie {new_movie_obj.movie_name} added successfully!"
            app.logger.info(message)
            return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 201

        message = f"Movie {new_movie_obj.movie_name} already exists."
        return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 400

    return render_template('add_movie.html',
                           user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    This route will display a form allowing for the updating
    of details of a specific movie. Update requires a user id,
    this way only registered users can update the movies in
    the database (it also allows tracking who made the changes).

    * If a GET request is made, it renders the update_movie.html
    template with a form to update the movie details.
    - The form is pre-filled with the current movie details
      retrieved from the database (with the given movie_id
      parameter in the URL).

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
        app.logger.info("POST request to update movie details"
                        "by {user_id} for movie {movie_id}")

        movie_to_update = data_manager.get_movie(movie_id)
        if movie_to_update:
            for key, value in request.form.items():
                if hasattr(movie_to_update, key) and value:
                    setattr(movie_to_update, key, value)

        updated_movie_name = data_manager.update_movie(movie_to_update)

        if updated_movie_name:
            status = "Movie updated"
            message = f"Movie {updated_movie_name} updated successfully!"
            app.logger.info(message)
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

    movie = data_manager.get_movie(movie_id)
    return render_template('update_movie.html',
                            user_id=user_id,
                            movie_id=movie_id,
                            movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """
    Upon visiting this route, a specific movie will be removed
    from a user’s favorite movie list.

    * Only registered users can delete movies from the database
    """
    if request.method == "POST":
        app.logger.info("POST request to delete movie"
                        "by {user_id} for movie {movie_id}")
        deleted_movie = data_manager.delete_movie(user_id, movie_id)
        if deleted_movie:
            status = "Movie deleted"
            message = f"Movie {deleted_movie.movie_name} deleted successfully!"
            app.logger.info(message)
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

    # If a GET request is made, render the delete_movie.html
    movie = data_manager.get_movie(movie_id)
    return render_template('delete_movie.html',
                            user_id=user_id,
                            movie_id=movie_id,
                            movie_name=movie.movie_name)


@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    """
    Returns the details of a specific movie.
    """
    app.logger.info(f"Movie details for movie {movie_id} accessed")
    try:
        movie = data_manager.get_movie(movie_id)
        if movie:
            return render_template('movie_info.html',
                                    movie=movie), 200
    except Exception as e:
        app.logger.error(f"Error fetching movie: {e}")
        return render_template('redirect.html',
                               status='Error 500',
                               message=e), 500

    message = "Movie not found."
    return render_template('movie_info.html',
                               message=message), 404


@app.route('/about')
def about():
    """
    Returns a render of the 'about.html' template with information
    about the application.
    """
    return render_template('about.html'), 200


# [Extra] Define the routes for error handling:

@app.errorhandler(404)
def not_found(error):
    """
    Returns a 404 error message for any invalid URL.
    """
    status = "Error 404"
    message = "This URL is not valid."
    return render_template("redirect.html",
                           status=status,
                           message=message), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Returns a 500 error message for any server errors.
    """
    status = "Error 500"
    return render_template("redirect.html",
                        status=status ,error=error), 500

# [Step 3] Define the main function to run the Flask application

if __name__ == '__main__':
    URL = 'http://127.0.0.1:5000/'
    webbrowser.open_new(URL)
    app.run(port=5000, debug=True)
