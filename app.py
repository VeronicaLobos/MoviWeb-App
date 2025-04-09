"""
This is a Flask application that connects to a SQLite database
and manages user and movie data using SQLAlchemy.
* Creates the database and tables if they don't exist.
* It defines several API endpoints to interact with the database,
by calling the methods of the DataManagerSQLite class:
- get_all_users: Retrieves all users from the database.
- get_user_movies: Retrieves all movies for a given user.
- add_user: Adds a new user to the database.
- add_movie: Adds a new movie to the database.
- update_movie: Updates an existing movie in the database.
- delete_movie: Deletes a movie from the database by its ID.
"""


from flask import Flask, jsonify, request, render_template
import os
import webbrowser
from data_models import db, User, Movie
from datamanager.data_manager_sqlite import DataManagerSQLite

# Initialize and configure the Flask application
app = Flask(__name__, static_folder='_static')

# Configure the SQLAlchemy database URI
database_path = os.path.join(os.path.dirname(__file__),'data','moviewebapp.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

# Initialize the SQLAlchemy instance with the Flask app
db.init_app(app)

# Initialize the DataManagerSQLite instance, passing the app and database path
data_manager = DataManagerSQLite(app, db)

# ...if the database file doesn't exist, create it
with app.app_context():
    if not os.path.exists(database_path):
        db.create_all()
        # Create the tables if they don't exist
        if db.session.query(User).count() == 0:
            db.create_all()
        if db.session.query(Movie).count() == 0:
            db.create_all()


## API endpoints

@app.route('/')
def home():
    """
    Renders the home page of the application.
    """
    message = "Welcome to the Movie Web App!"

    return render_template('home.html', message=message)


@app.route('/users') ## Works ######
def list_users():
    """
    Returns a list of all users in the database.
    """
    user_list = data_manager.get_all_users()

    if user_list:
        return render_template('users.html', user_list=user_list), 200
    else:
        message = "No users found."
        return render_template('users.html', message=message), 404


@app.route('/users/<int:user_id>')
def list_user_movies():
    """
    Returns a list of all movies associated with a given user.

    - Retrieves the user ID from the request parameters.
    - Queries the database for all movies associated with the user
    by calling the get_user_movies method of the DataManagerSQLite instance.

    Returns a JSON response with the list of movie names,
    or an error message if no movies are found.
    """
    user_id = request.args.get('user_id')
    user_movies = data_manager.get_user_movies(user_id)

    if user_movies:
        return jsonify([movie.movie_name for movie in user_movies]), 200
    else:
        return jsonify({"message": "No movies found for this user."}), 404


@app.route('/add_user', methods=['GET', 'POST']) ## Works ######
def add_user():
    """
    Adds a new user to the database.

    If a GET request is made, it renders the  add_user.html template.

    If a POST request is made, it retrieves the user data from the request,
    creates a new User object with it, and adds it to the database by calling
    the add_user method of the DataManagerSQLite instance.

    Returns a JSON response with a success message,
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

    If a POST request is made, it passes the user ID from the request URL to check
    if the user exists in the database. If the user exists,
    it retrieves the movie data from the request form,
    creates a new Movie object with it, and adds it to the database by calling
    the add_movie method of the DataManagerSQLite instance.

    Returns a JSON response with a success message,
    or an error message if the movie already exists.
    """
    if request.method == 'POST':

        ## Check if the user exists
        users_list = data_manager.get_all_users()
        for user in users_list:
            if user.user_id == user_id:
                break
            else:
                return jsonify({"message": "User does not exist."}), 404

        ## If the user exists, get the data from the form and create a new Movie object
        new_movie_obj = Movie(
            movie_name=request.form.get('movie_name'),
            director=request.form.get('director'),
            year=request.form.get('year'),
            rating=request.form.get('rating'),
        )

        # Call the add_movie method to add the new movie to the database
        new_movie_exists = data_manager.add_movie(new_movie_obj)

        # Check if the movie already exists, if not, add the movie
        if new_movie_exists:
            # new_movie_exists is True if the movie was added successfully
            return jsonify({"message": f"Movie {new_movie_obj.movie_name} added successfully!"}), 201
        else:
            # new_movie_exists is None if the movie already exists
            return jsonify({"message": f"Movie {new_movie_obj.movie_name} already exists."}), 400

    return render_template('add_movie.html')


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
    pass


if __name__ == '__main__':
    # Run the Flask application and open the web browser
    url = 'http://127.0.0.1:5002/'
    webbrowser.open_new(url)
    app.run(port=5002, debug=True)