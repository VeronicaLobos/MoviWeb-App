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

    def get_user_name(self, user_id: int) -> str:
        """
        Retrieves the user_name associated with a given user ID.

        Parameters:
            user_id (int): The ID of the user whose name is to be retrieved.

        Returns:
            str: The user_name associated with the given user ID,
            or None if the user does not exist.
        """
        # Get the user object by ID
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return user.user_name
        else:
            return None


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


    def get_movie(self, movie_id: int) -> Movie:
        """
        Retrieves a movie from the database.

        Parameters:
            movie_id (int): The ID of the movie to be retrieved.

        Returns:

        """
        # Get the movie object by ID
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        if movie:
            return movie
        else:
            return None


    def get_all_movies(self):
        """
        Retrieves all movies from the database.

        - Queries the database for all movies.

        Returns:
            list: A list of Movie objects,
            or an empty list if no movies are found.
        """
        # Get all movies from the database
        movies = Movie.query.all()
        if movies:
            return movies
        else:
            return []


    def get_user_movies(self, user_id: int) -> list:
        """
        Retrieves all movies associated with a given user.

        Parameters:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            a list of tuples: (movie_data: Movie, rating: float),
            or an empty list if no movies are found.
        """
        # Get the movies associated with the user id in the UserMovies table
        user_movies = UserMovie.query.filter_by(user_id=user_id).all()

        if user_movies:
            # Return the movies associated with the user
            # with the rating included in the UserMovies association
            return [(movie.movie_relation, movie.rating) for movie in user_movies]
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


    def update_rating(self, user_id, movie_id, rating) -> bool:
        """
        Updates the rating of a movie in the UserMovie table.

        Parameters:
            user_id (int): The ID of the user associated with the movie.
            movie_id (int): The ID of the movie to be updated.
            rating (float): The new rating of the movie by the user.

        Returns:
            True if the movie was updated successfully,
            None if the movie does not exist.
        """
        # Fetch the user_movie object from the UserMovie table
        user_rating = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if user_rating:
            # Update the rating of the movie
            user_rating.rating = rating
            self.db.session.commit()
            return True


    def update_movie(self, updated_movie: Movie) -> bool:
        """
        Updates the movie details in the database.

        - updates the movie details in the database.

        Parameters:
            updated_movie (Movie): The Movie object with updated details.

        Returns:
            str: The name of the updated movie,
            None if the movie does not exist.
        """
        movie_to_update = Movie.query.filter_by(movie_id=updated_movie.movie_id).first()
        if movie_to_update:
            self.db.session.commit()
            return movie_to_update.movie_name
        else:
            print(f"Movie with ID {updated_movie.movie_id} not found.")
            return None



    def delete_movie(self, user_id, movie_id) -> str:
        """
        Deletes a row from the UserMovie table based on user_id and movie_id.

        Parameters:
            user_id (int): The ID of the user associated with the movie.
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            bool: True if the movie was deleted successfully, False otherwise.
        """
        # Fetch the movie title from the Movie table with the given movie_id
        movie_name = Movie.query.filter_by(movie_id=movie_id).first()
        print(movie_name.movie_name)

        # Fetch the movie object from the UserMovie table
        user_movie = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if user_movie:
            self.db.session.delete(user_movie)
            self.db.session.commit()
            return movie_name
        else:
            print(f"Movie with ID {movie_id} not found for user with ID {user_id}.")
            return False
