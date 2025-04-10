"""
This is a Flask application that connects to a SQLite database
and manages user and movie data using SQLAlchemy.
* Creates the database and tables if they don't exist.
* It defines several API endpoints to interact with the database,
by calling the methods of the DataManagerSQLite class.
"""

"""
Step 1. Import necessary modules
"""

from flask import Flask, request, render_template
import os
import webbrowser
from data_models import db, User, Movie
from datamanager.data_manager_sqlite import DataManagerSQLite
from omdb_data_fetcher import get_new_movie_data as data_fetcher

"""
Step 2. Initialize the Flask application 
and SQLAlchemy database connection:
- Initialize and configure the Flask application.............[√]
- Create the database path...................................[√]
- Set the SQLAlchemy database URI............................[√]
- Initialize the SQLAlchemy instance with the Flask app......[√]
- Initialize the DataManagerSQLite instance by passing
the app and database.........................................[√]
- Create the database and tables if they don't exist.........[√]
"""

app = Flask(__name__, static_folder='_static')

database_path = os.path.join(os.path.dirname(__file__),
                             'data','moviewebapp.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

db.init_app(app)
data_manager = DataManagerSQLite(app, db)

with app.app_context():
    if not os.path.exists(database_path):
        db.create_all()
        if db.session.query(User).count() == 0:
            db.create_all()
        if db.session.query(Movie).count() == 0:
            db.create_all()


"""
Step 3. Define the API endpoints:
- 1. Define the home route ..................[√]
- 2. Define the route to list all users......[√]
- 3. Define the route to list user movies....[√]
- 4. Define the route to add a user..........[√]
- 5. Define the route to add a movie.........[ ]
- 6. Define the route to update a movie......[ ]
- 7. Define the route to delete a movie......[ ]
"""

@app.route('/home')
def home():
    """
    Renders the home page of the application with a welcome message.
    and buttons to navigate to different sections of the application.
    """
    message = "Welcome to the Movie Web App!"

    return render_template('home.html',
                           message=message)


@app.route('/users')
def list_all_users():
    """
    Returns a render of the users.html template with
    a list of all users in the database, each linked to
    their respective movie lists.
    If no users are found, it returns a 404 error with a message.
    """
    user_list = data_manager.get_all_users()

    if user_list:
        return render_template('users.html',
                               user_list=user_list), 200
    else:
        message = "No users found in the database."
        return render_template('users.html',
                               message=message), 404


@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    """
    Returns a list of all movies associated with a given user.

    - Queries the database for all movies associated with the user
    by calling the get_user_movies method of the DataManagerSQLite instance.

    Returns a render of the user_movies.html template with
    the list of movies associated with the user.
    """
    user_movies = data_manager.get_user_movies(user_id)

    if user_movies:
        return render_template('user_movies.html',
                               user_id=user_id,
                               user_movies=user_movies), 200
    else:
        message = "No movies found for this user."
        return render_template('user_movies.html',
                               user_id=user_id,
                               message=message), 404


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Adds a new user to the database.

    If a GET request is made, it renders the  add_user.html template.

    If a POST request is made, it retrieves the user data from the request,
    creates a new User object with it, and adds it to the database by calling
    the add_user method of the DataManagerSQLite instance.

    Returns a render of the add_user.html template with a success message,
    or an error message if the user already exists.
    """
    if request.method == 'POST':
        # Get the data from the form (string) and create a new User object
        new_user_obj = User(
            user_name=request.form.get('user_name')
        )
        # Call the add_user method to add the new user to the database
        new_user_exists = data_manager.add_user(new_user_obj)
        # Check if the user already exists, if not, add the user
        if new_user_exists:
            # new_user_exists is True if the user was added successfully
            message = f"User {new_user_obj.user_name} added successfully!"
            return render_template('add_user.html', message=message), 201
        else:
            # new_user_exists is None if the user already exists
            message = f"User {new_user_obj.user_name} already exists."
            return render_template('add_user.html', message=message), 400

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Adds a new movie to the database.

    If a GET request is made, it renders the add_movie.html template.

    If a POST request is made:
    - it retrieves the movie name and the rating
    by the user associated to that id from the request form.
    - calls data_fetcher to fetch the movie data from the OMDb API.
    - a Movie object is returned (if the movie is found in the API).
    - calls the add_movie method of the DataManagerSQLite instance
    to add the movie to the database.
        - If the movie already exists, it will not be added again.
        - It checks if there is already a rating for the movie
        with that user_id and movie_id in the UserMovies table.

    Returns:
        If the movie is added successfully, it returns a render
        containing a message informing the user with the resulting
        operation.
    """
    if request.method == 'POST':
        ## Create a new Movie object
        movie_name = request.form.get('movie_name')
        rating = request.form.get('rating')
        new_movie_obj = data_fetcher(movie_name)

        # If new_movie_obj is None, it means the movie was not found
        if new_movie_obj is None:
            message = f"Movie {movie_name} not found."
            return render_template('add_movie.html',
                                   message=message), 404

        # If the movie was found, a Movie object is returned
        # and can be added to the database
        new_movie_exists = data_manager.add_movie(new_movie_obj,
                                                  user_id, rating) #TODO!!!!

        # Check if the movie was added successfully:
        # new_movie_exists is True if the movie was added
        # successfully or False if the movie already exists
        if new_movie_exists:
            message = (f"Movie {new_movie_obj.movie_name} added successfully"
                       f"with rating {rating}!")
            return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 201
        else:
            message = f"Movie {new_movie_obj.movie_name} already exists."
            return render_template('add_movie.html',
                                   message=message,
                                   user_id=user_id), 400

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    This route will display a form allowing for the updating
    of details of a specific movie in a user’s list.
    """
    pass


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    """
    Upon visiting this route, a specific movie will be removed
    from a user’s favorite movie list.
    """
    deleted_movie = data_manager.delete_movie(user_id, movie_id)
    if deleted_movie:
        message = f"Movie {deleted_movie.movie_name} deleted successfully!"
        return render_template('delete_movie.html',
                               message=message,
                               user_id=user_id,
                               movie_id=movie_id), 200
    else:
        message = f"Movie with ID {movie_id} not found."
        return render_template('delete_movie.html',
                               message=message,
                               user_id=user_id,
                               movie_id=movie_id), 404


if __name__ == '__main__':
    # Run the Flask application and open the web browser
    url = 'http://127.0.0.1:5002/home'
    webbrowser.open_new(url)
    app.run(port=5002, debug=True)