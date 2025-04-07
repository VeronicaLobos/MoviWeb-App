"""
DataManagerSQLite
This module provides an interface for managing data in a SQLite database.
"""
from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface

class DataManagerSQLite(DataManagerInterface):
    def __init__(self, db_file_name):
        """
        Initializes the DataManagerSQLite with the database path.

        Args:
            db_file_name (str): The path to the SQLite database file.
        Attributes:
            self.db: SQLAlchemy instance for database operations.
        Methods:
            get_all_users: Retrieves all users from the database.
            get_user_movies: Retrieves all movies for a given user.
        """
        self.db = SQLAlchemy(db_file_name)

    def get_all_users(self):
        """
        Retrieves all users from the database.
        """
        pass

    def get_user_movies(self, user_id):
        """
        Retrieves all movies for a given user.
        """
        pass

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
