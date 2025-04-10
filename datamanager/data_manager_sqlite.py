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
from data_models import User, Movie, UserMovie

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

        Returns a list of Movie objects associated with a given user,
        with the rating included in the UserMovie association.
        or an empty list if the user does not exist or has no movies.
        """
        # Get the movies associated with the user id in the UserMovies table
        user_movies = UserMovie.query.filter_by(user_id=user_id).all()
        if user_movies:
            # Return the movies associated with the user
            # with the rating included in the UserMovies association
            return [movie_obj.movie_relation for movie_obj in user_movies]
        else:
            return []


    ## Any write operation will return True or None
    ## TODO: Change return None to return False

    def add_user(self, new_user: User) -> bool:
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


    def add_movie(self, new_movie: Movie, user_id: int, rating: float) -> bool:
        """
        Adds a new movie to the database.

        - Checks if the movie already exists in the database.
        - If the movie does not exist, it adds the new movie to the database.
        - Checks if the user already has a rating for this movie.
        - Creates a new UserMovies association

        Parameters:
            new_movie (Movie): The Movie object to be added.
            user_id (int): The ID of the user associated with the movie.
            rating (float): The rating of the movie by the user.
        Returns:
            None if the movie already exists.
            True if the movie was added successfully.
        """

        # Step 1. Check if the movie already exists in the movies table
        movie_exists = Movie.query.filter_by(movie_name=new_movie.movie_name).first()

        # Step 2. If the movie does not exist, first, add it to the database
        if movie_exists is None:
            # Add the new movie to the database
            self.db.session.add(new_movie)
            self.db.session.commit()

        # Step 3. Get the movie ID of the existing/newly-added movie
        movie = Movie.query.filter_by(movie_name=new_movie.movie_name).first()

        # Step 3.1. Check if the user already has a rating for this movie
        user_rating_exists = UserMovie.query.filter_by(user_id=user_id, movie_id=movie.movie_id).first()

        # Step 3.2. If the user already has a rating for this movie, return None
        if user_rating_exists:
            return None

        # Step 4. If the user does not have a rating for this movie,
        elif user_rating_exists is None:
            # Create a new UserMovie association
            user_rating = UserMovie(user_id=user_id, movie_id=movie_exists.movie_id, rating=rating)
            # And add the new UserMovie association to the database
            self.db.session.add(user_rating)
            self.db.session.commit()
            return True


    def update_movie(self, user_id, movie_to_update: str, movie_obj: Movie) -> bool:
        """
        Updates an existing movie in the database.

        - Checks if the movie exists in the database.
        - If the movie exists, it updates the movie details.

        Parameters:
            user_id (int): The ID of the user associated with the movie.
            movie_to_update (str): The name of the movie to be updated.
            movie_obj (Movie): The updated Movie object.

        Returns:
            True if the movie was updated successfully,
            None if the movie does not exist.
        """



    def delete_movie(self, user_id, movie_id):
        """
        Deletes a movie from the database by its ID.
        """
        # Find the related UserMovie entry
        user_movie = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if user_movie:
            # Delete the UserMovie entry
            self.db.session.delete(user_movie)
            self.db.session.commit()
            return True
        else:
            return None

