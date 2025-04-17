"""
DataManagerSQLite is a DAL (Data Access Layer) module for managing data
in a SQLite database.

It defines a DataManagerSQLite class that interacts with the database
using SQLAlchemy.

When an object of this class is created, it initializes a SQLAlchemy
instance with the provided database file name.

SQLAlchemy ORM is a class provided by the flask_sqlalchemy extension.
It acts as a wrapper around SQLAlchemy, providing a simplified and
Flask-integrated way to interact with databases.
The class provides methods to perform CRUD (Create, Read, Update, Delete)
operations on the database, including:
- Retrieving a specific username
- Retrieving all users and their details
- Retrieving a specific movie and its details
- Retrieving all movies and their details
- Retrieving all movies associated with a specific user
  and their ratings
- Adding a new user
- Adding a new movie, and a rating for a specific user
- Updating the rating of a movie for a specific user
- Updating the details of a movie
- Deleting a movie from the user's list of rated movies,
  and deleting the movie from the database if no other
  users have rated it.
"""
from datamanager.data_manager_interface import DataManagerInterface
from data_models import User, Movie, UserMovie

class DataManagerSQLite(DataManagerInterface):
    """
    DataManagerSQLite is a class for managing data in a SQLite database.
    """
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
            user_id (int): The ID of the user whose name is to
                           be retrieved.

        Returns:
            str: The user_name associated with the given user ID,
            None: if the user does not exist, with a message printed
                  to the console.
        """
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            print(f"User with ID {user_id} not found.")
            return None
        return user.user_name


    def get_all_users(self) -> list:
        """
        Retrieves all users from the database.

        Returns:
            list: A list of User objects,
            or an empty list if no users are found.
        """
        users = User.query.all()
        return users


    def get_movie(self, movie_id: int) -> Movie:
        """
        Retrieves a specific movie from the database.

        Parameters:
            movie_id (int): The ID of the movie to be retrieved.

        Returns:
            Movie: The Movie object associated with the given
            movie ID, or None if the movie does not exist.
        """
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        return movie


    def get_all_movies(self) -> list:
        """
        Retrieves all movies from the database.

        Returns:
            list: A list of Movie objects,
            or an empty list if no movies are found.
        """
        movies = Movie.query.all()
        return movies


    def get_user_movies(self, user_id: int) -> list:
        """
        Retrieves all movies associated with a given user id.

        - Includes the rating of each movie by the user.

        Parameters:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            a list of tuples: (movie_data: Movie, rating: float),
            or an empty list if no movies are found.
        """
        user_movies = UserMovie.query.filter_by(user_id=user_id).all()

        return [(movie.movie_relation, movie.rating) for movie in user_movies]


    def add_user(self, new_user: User) -> bool:
        """
        Adds a new user to the database.

        Parameters:
            new_user (User): The User object to be added.

        - Checks if the user already exists in the database.
        - If the user does not exist, it adds the new user to the database.

        Returns:
            True if the user was added successfully,
            False if the user already exists.
        """
        user_exists = User.query.filter_by(user_name=new_user.user_name).first()
        if user_exists:
            print(f"User '{new_user.user_name}' already exists.")
            return False

        self.db.session.add(new_user)
        self.db.session.commit()
        return True


    def add_movie(self, new_movie: Movie, user_id: int) -> bool:
        """
        Adds a new movie to the database.

        - Checks if the movie already exists in the database.
        - If the movie does not exist, it adds the new movie to
          the database.
        - If the movie already exists (or was added), it retrieves
          the movie ID.
        - Checks if the user already has a relationship for this movie:
            - If the user has a relationship, it returns False.
            - If the user does not have a relationship, it creates a new
              UserMovie association and adds it to the database.

        Parameters:
            new_movie (Movie): The Movie object to be added.
            user_id (int): The ID of the user associated with the
            movie.
        Returns:
            False if the movie already exists AND the given user_id
            has a relationship for this movie,
            True if the movie was added successfully, OR
            the movie was already in the database and the user_id
            already had a relationship for this movie (it is not updated).
        """
        movie_exists = (Movie.query.filter_by(movie_name=new_movie.movie_name).
                        first())

        if movie_exists is None:
            self.db.session.add(new_movie)
            self.db.session.commit()

        movie = (Movie.query.filter_by(movie_name=new_movie.movie_name).
                        first())

        user_relationship_exists = (UserMovie.query.filter_by(user_id=user_id,
                                                       movie_id=movie.movie_id).
                              first())

        if user_relationship_exists is None:
            user_relationship = UserMovie(user_id=user_id,
                                    movie_id=movie.movie_id)
            self.db.session.add(user_relationship)
            self.db.session.commit()
            return True

        print(f"User '{user_id}' already has {movie.movie_name} "
              f"in their list'.")
        return False


    def update_rating(self, user_id, movie_id, rating) -> bool:
        """
        Updates the rating of a movie in the UserMovie table.

        Parameters:
            user_id (int): The ID of the user associated with the movie.
            movie_id (int): The ID of the movie to be updated.
            rating (float): The new rating of the movie by the user.

        Returns:
            True if the movie was updated successfully,
            False if the movie does not exist.
        """
        user_rating = UserMovie.query.filter_by(user_id=user_id,
                                                movie_id=movie_id).first()

        if user_rating:
            user_rating.rating = rating
            self.db.session.commit()
            return True


    def update_movie(self, updated_movie: Movie) -> bool:
        """
        Updates the movie details in the database.

        Parameters:
            updated_movie (Movie): The Movie object with
            updated details.

        Returns:
            str: The name of the updated movie,
            None if the movie does not exist.
        """
        movie_to_update = (Movie.query.filter_by(movie_id=updated_movie.movie_id)
                           .first())
        if movie_to_update:
            self.db.session.commit()
            return movie_to_update.movie_name
        else:
            print(f"Movie with ID {updated_movie.movie_id} not found.")
            return False


    def delete_movie(self, user_id, movie_id) -> str:
        """
        Deletes a row from the UserMovie table based
        on user_id and movie_id.
        * If the movie is not rated by any other user,
        it deletes the movie from the Movie table as well.

        Parameters:
            user_id (int): The ID of the user associated
                           with the movie.
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            bool: True if the movie was deleted successfully,
                  False otherwise.
        """
        movie_name = (Movie.query.filter_by(movie_id=movie_id).
                      first())
        print(movie_name.movie_name)

        # Fetch the movie object from the UserMovie table
        user_movie = UserMovie.query.filter_by(user_id=user_id,
                                    movie_id=movie_id).first()

        if user_movie:
            self.db.session.delete(user_movie)
            self.db.session.commit()

            # Check if other users have rated the movie
            other_users = (UserMovie.query.filter_by(movie_id=movie_id).
                           all())

            if not other_users:
                movie = (Movie.query.filter_by(movie_id=movie_id).
                         first())
                self.db.session.delete(movie)
                self.db.session.commit()
                print(f"Movie '{movie_name.movie_name}' "
                      f"deleted successfully.")
            else:
                print(f"Movie '{movie_name.movie_name}' "
                      f"still has ratings from other users.")
            return movie_name

        else:
            print(f"Movie with ID {movie_id} not found for "
                  f"user with ID {user_id}.")
            return False
