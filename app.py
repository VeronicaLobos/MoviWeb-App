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
    return jsonify({"message": "Welcome to the Movie Web App!"}), 200


@app.route('/users')
def list_user():
    """
    Returns a list of all users in the database.
    """
    users_list = data_manager.get_all_users()

    if users_list:
        return jsonify([user.user_name for user in users_list]), 200
    else:
        return jsonify({"message": "No users found."}), 404


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


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Adds a new user to the database.

    If a GET request is made, it renders the add_user.html template.

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
            return jsonify({"message": f"User {new_user_obj.user_name} added successfully!"}), 201
        else:
            # new_user_exists is None if the user already exists
            return jsonify({"message": f"User {new_user_obj.user_name} already exists."}), 400

    return render_template('add_user.html')




if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)