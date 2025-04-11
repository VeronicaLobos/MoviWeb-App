"""
*** Movie Web App ***
========================

This is a Restful API for a Movie Web App that allows users to
manage a list with their favorite movies and give a rating to
each movie, as well as retrieve movie details from the OMDb API
and edit the movie information.

This program is a learning project for the Software Engineering
Bootcamp at MasterSchool. It showcases what I have learned
about Python programming, API and web development.
A step-by-step guide is included to help you understand how the
code has been implemented.

Author: https://github.com/VeronicaLobos
Date: 2025-April-11


App Key Features:
 - Restful API architecture with CRUD operations for managing
    movies and users.
 - The API is built using Flask and SQLAlchemy, and it uses
    SQLite as the database.
 - Endpoints for adding, updating, and deleting movies, adding
    users, adding user ratings, and retrieving movie details
    and user ratings.
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
#     · Adds a new movie and user rating to the db
# - 6. Define the route to update a movie......................[√]
#     · Updates a movie information in the db
# - Extra. Define the route to update a rating.................[√]
#     · Updates a user rating for a movie in the db
# - 7. Define the route to delete a movie......................[√]
#     · Deletes a movie from the user's list,
#       and from the db if no other user has rated it
# - Extra. Define the route to get movie details...............[√]
#     · Fetches a movie's details from the db

@app.route('/home')
def home():
    """
    Renders the home page of the application with a welcome
    message, buttons to navigate to different sections
    of the application, and all movie posters in the database
    displayed in a grid format with links to their details.
    """
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
    along with the user rating for each movie.
    Each  movie is linked to its details page.
    Each  movie has a button for:
    · updating the movie information
    · updating the user rating
    · deleting the movie from the user's list

    - Queries the database for all movies associated with the
    user by calling the get_user_movies method of the
    DataManagerSQLite instance.
    - Queries the database for the user_name associated with
    the user_id.

    Returns a render of the user_movies.html template with
    the list of movies containing the movie name and rating,
    the user_id and the user_name.
    If no movies are found for the user, it renders the template
    with a message indicating that no movies were found.
    """
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name(user_id)

    if user_movies:
        # Extract the movie (Movie) and their ratings (int)
        user_movies = [(movie[0], movie[1]) for movie in user_movies]
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
            return render_template('add_user.html', message=message), 201

        message = f"User {new_user_obj.user_name} already exists."
        return render_template('add_user.html', message=message), 400

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Adds a new movie to the database.

    * If a GET request is made, it renders the add_movie.html
     template with a form to add a new movie.
     - Only users with a user_id can add movies to the database.

    * If a POST request is made:
    - It retrieves the movie name and the rating by the user
      associated to that id from the request form.
    - Calls data_fetcher to fetch the movie data from the OMDb API.
    - A Movie object is returned (if the movie is found in the API).
    - Calls the add_movie method of the DataManagerSQLite instance
      to add the movie to the database:
        - If the movie already exists, it will not be added again.
        - It checks if there is already a rating for the movie
          with that user_id and movie_id in the UserMovies table.
        - If the user already rated the movie, it will not be added
          again.

    Returns:
        If the movie is added successfully, it returns a render
        containing a message informing the user with the resulting
        operation.
        Note: by providing the user_id in the render_template,
        it allows the user to resubmit the form. This avoids
        the flask app from crashing because the route
        is not found.
    """
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        rating = request.form.get('rating')
        new_movie_obj = data_fetcher(movie_name)

        # If new_movie_obj is None, it means the movie was not found, or
        # there was an error fetching the data, or no internet connection
        if new_movie_obj is None:
            message = f"Movie {movie_name} not found."
            return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 404

        # If the movie was found, a Movie object is returned
        # and can be added to the database
        new_movie_exists = data_manager.add_movie(new_movie_obj,
                                                  user_id, rating)

        if new_movie_exists:
            message = (f"Movie {new_movie_obj.movie_name} added successfully"
                       f" with rating {rating}!")
            return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 201

        message = f"Movie {new_movie_obj.movie_name} already exists."
        return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 400

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_rating/<int:movie_id>', methods=['GET', 'POST'])
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


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
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
    URL = 'http://127.0.0.1:5002/home'
    webbrowser.open_new(URL)
    app.run(port=5002, debug=True)
