"""
DataManagerInterface: An Interface for Data Manager classes.
This interface defines the methods that any data manager class must implement.
This is useful for ensuring that all data manager classes have a consistent
interface, making it easier to switch between different data managers
without changing the rest of the code.

Polymorphism: By providing a common interface for different data manager
classes, we can use polymorphism to switch between different implementations
without changing the code that uses them.
This allows for greater flexibility and maintainability in the codebase, and
makes it easier to add new data manager classes in the future.
"""

from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """
    An interface for data manager classes.
    """
    @abstractmethod
    def get_user_name(self, user_id):
        """
        Retrieves the user_name associated with a given user ID.
        """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users from the database.
        """

    @abstractmethod
    def get_movie(self, movie_id):
        """
        Retrieves a movie from the database.
        """

    @abstractmethod
    def get_all_movies(self):
        """
        Retrieves all movies from the database.
        """

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves all movies for a given user from the database.
        """

    @abstractmethod
    def add_user(self, user):
        """
        Adds a new user to the database.
        """

    @abstractmethod
    def add_movie(self, movie, user_id, rating):
        """
        Adds a new movie to the database.
        """

    @abstractmethod
    def update_rating(self, user_id, movie_id, rating):
        """
        Updates an existing movie in the database.
        """

    @abstractmethod
    def update_movie(self, updated_movie) -> bool:
        """
        Updates the movie details in the database.
        """

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """
        Deletes a movie from the database.
        """
