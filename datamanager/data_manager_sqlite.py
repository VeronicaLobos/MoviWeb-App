"""
DataManagerSQLite is a DAL (Data Access Layer) module for managing data
in a SQLite database.

It defines a DataManagerSQLite class that interacts with the database using
SQLAlchemy.

When an object of this class is created, it initializes a SQLAlchemy
instance with the provided database file name.

SQLAlchemy ORM is a class provided by the flask_sqlalchemy extension.
It acts as a wrapper around SQLAlchemy, providing a simplified and
Flask-integrated way to interact with databases.
"""
from datamanager.data_manager_interface import DataManagerInterface
from data_models import User, Movie, UserMovies

class DataManagerSQLite(DataManagerInterface):
    def __init__(self, app, database):
        """
        Parameters:
            app (Flask): The Flask application instance.
            database (str): The path to the SQLite database file.
        Attributes:
            self.db: SQLAlchemy instance for database operations.
        """
        self.db = database
        self.app = app


    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns a list of User objects,
        or an empty list if no users are found.
        """
        users = User.query.all()
        if users:
            return users
        else:
            return []


    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a given user.

        Returns a list of Movie objects associated with a given user,
        or an empty list if the user does not exist or has no movies.
        """
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            movies = UserMovies.query.filter_by(user_id=user.user_id).all()
            if movies:
                return [movie.movie_relation for movie in movies]
            else:
                return []
        else:
            return []


    def add_user(self, user):
        """
        Adds a new user to the database.
        """
        pass

    def add_movie(self, movie):
        """
        Adds a new movie to the database.
        """
        pass

    def update_movie(self, movie):
        """
        Updates an existing movie in the database.
        """
        pass

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database by its ID.
        """
        pass

    #####

    def get_user(self, user_id):
        """
        Retrieves a user from the database by its ID.
        """
        pass

    def get_movie(self, movie_id):
        """
        Retrieves a movie from the database by its ID.
        """
        pass
