from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy instance, which will be used to initialize the database
# and manage the models in app.py
db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        user_id (int): The unique identifier for the user.
        user_name (str): The username of the user.
    """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False)

    # Establish relationship with UserMovies table
    user_movies = db.relationship('UserMovie', backref='user_relation')

    def __str__(self):
        return f"User: {self.user_name}"


class Movie(db.Model):
    """
    Represents a movie in the database.

    Attributes:
        movie_id (int): The unique identifier for the movie.
        movie_name (str): The name of the movie.
        director (str): The director of the movie.
        year (int): The release year of the movie.
        genre (str): The genre of the movie.
        poster_url (str): The URL of the movie poster.
    """
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    director = db.Column(db.String)
    genre = db.Column(db.String)
    poster_url = db.Column(db.String)
    plot = db.Column(db.String)

    # Establish relationship with UserMovies table
    user_movies = db.relationship('UserMovie', backref='movie_relation')

    def __str__(self):
        return (f"Movie ID: {self.movie_id}, "
                f"Movie name: {self.movie_name}, "
                f"Director: {self.director}, "
                f"Year: {self.year}, "
                f"Genre: {self.genre}, "
                f"Poster URL: {self.poster_url}",
                f"Plot: {self.plot}")


class UserMovie(db.Model):
    """
    Associates a user with one or several movies (one-to-many
    relationship).

    Attributes:
        id (int): The unique identifier for the association.
        user_id (int): The unique identifier for the user.
        movie_id (int): The unique identifier for the movie.
        rating (float): The rating of the movie by the user.
    """
    __tablename__ = 'user_movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,
                db.ForeignKey('users.user_id'), nullable = False)
    movie_id = db.Column(db.Integer,
                db.ForeignKey('movies.movie_id'), nullable = False)
    rating = db.Column(db.Float)


    def __str__(self):
        return (f"User ID: {self.user_id}, Movie ID: {self.movie_id},"
                f" Rating: {self.rating}")
