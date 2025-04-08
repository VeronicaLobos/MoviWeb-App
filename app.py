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


from flask import Flask
import os
from data_models import db, User, Movie

# Initialize and configure the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy database URI
database_path = os.path.join(os.path.dirname(__file__),'data','db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

# Initialize the SQLAlchemy instance with the Flask app
db.init_app(app)

# If the database file doesn't exist, create it
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
def get_user(user_id):
    """
    Endpoint to get user information by user ID.
    """
    user = User.query.get(user_id)
    if user:
        return str(user)
    else:
        return "User not found", 404


if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)