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
    def __init__(self, app, db):
        """
        Parameters:
            app (Flask): The Flask application instance.
            database (str): The path to the SQLite database file.
        Attributes:
            self.db: SQLAlchemy instance for database operations.
        """
        self.db = db
        self.app = app

    ## Any get operation will return a list of objects

    def get_all_users(self) -> list:
        """
        Retrieves all users from the database.

        - Queries the database for all users.

        Returns a list of User objects,
        or an empty list if no users are found.
        """
        users = User.query.all()
        if users:
            return users
        else:
            return []


    def get_user_movies(self, user_id: int) -> list:
        """
        Retrieves all movies associated with a given user.

        Parameters:
            user_id (int): The ID of the user whose movies are to be retrieved.

        - Checks if the user exists in the database.
        - If the user exists, it retrieves all movies associated with that user.

        Returns a list of Movie objects associated with a given user,
        or an empty list if the user does not exist or has no movies.
        """
        user_obj = User.query.filter_by(user_id=user_id).first()
        if user_obj:
            movie_obj_list = UserMovies.query.filter_by(user_id=user_id).all()
            if movie_obj_list:
                return [movie_obj.movie_relation for movie_obj in movie_obj_list]
            else:
                return []
        else:
            return []


    ## Any write operation will return True or None

    def add_user(self, new_user: object) -> bool:
        """
        Adds a new user to the database.

        Parameters:
            new_user (User): The User object to be added.

        - Checks if the user already exists in the database.
        - If the user does not exist, it adds the new user to the database.

        Returns:
            True if the user was added successfully,
            None if the user already exists.
        """
        # Check if the user already exists
        user_exists = User.query.filter_by(user_name=new_user.user_name).first()
        if user_exists:
            print(f"User '{new_user.user_name}' already exists.")
            return None

        # Add the new user to the database
        self.db.session.add(new_user)
        self.db.session.commit()
        return True


    def add_movie(self, movie_obj: object) -> bool:
        """
        Adds a new movie to the database.

        - Checks if the movie already exists in the database.

        Parameters:

        """
        movie_exists = Movie.query.filter_by(movie_name=movie_obj.movie_name).first()
        if movie_exists:
            print(f"Movie '{movie_obj.movie_name}' already exists.")
            return None

        self.db.session.add(movie_obj)
        self.db.session.commit()

        # Create a new UserMovies association
        pass

        return True


    def update_movie(self, user_id, movie_to_update: str, movie_obj: object) -> bool:
        """
        Updates an existing movie in the database.

        - Checks if the movie exists in the database.
        - If the movie exists, it updates the movie details.

        Parameters:
            movie_name (str): The name of the movie to be updated.
            movie_obj (Movie): The updated Movie object.

        Returns:
            True if the movie was updated successfully,
            None if the movie does not exist.
        """




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
