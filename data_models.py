from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

# Flask-SQLAlchemy instance
db = SQLAlchemy()


class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        user_name (str): The username of the user.
    """
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(String)

    def __repr__(self):
        """
        Returns a string representation of the user.
        This method is used for debugging and logging purposes.
        """
        return f"User(id={self.id}, name='{self.name}')"

    def __str__(self):
        """
        Returns a string representation of the user.
        This method is used to display the user information
        """
        return f"User: {self.user_name}"


class Movie(db.Model):
    """
    Represents a movie in the database.

    Attributes:
        id (int): The unique identifier for the movie.
        movie_name (str): The name of the movie.
        director (str): The director of the movie.
        year (int): The release year of the movie.
        rating (int): The rating of the movie.
    """
    __tablename__ = 'movies'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(String)
    director = db.Column(String)
    year = db.Column(Integer)
    rating = db.Column(Integer)

    def __repr__(self):
        """
        Returns a string representation of the movie.
        This method is used for debugging and logging purposes.
        """
        return (f"Movie(id={self.id}, name='{self.movie_name}', "
                f"director='{self.director}', year={self.year}, "
                f"rating={self.rating})")

    def __str__(self):
        """
        Returns a string representation of the movie.
        This method is used to display the movie information
        """
        return (f"Movie: {self.movie_name}, "
                f"Director: {self.director}, "
                f"Year: {self.year}, "
                f"Rating: {self.rating}")
