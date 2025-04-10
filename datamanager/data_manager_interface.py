"""
DataManagerInterface: An Interface for Data Manager classes.
This interface defines the methods that any data manager class must implement.
This is useful for ensuring that all data manager classes have a consistent
interface, making it easier to switch between different data managers
without changing the rest of the code.

Polymorphism: By providing a common interface for different data manager
classes, we can use polymorphism to switch between different implementations
without changing the code that uses them.
"""

from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_user_name(self, user_id):
        """
        Retrieves the user_name associated with a given user ID.
        """
        pass

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users from the database.
        """
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        """
        Retrieves a movie from the database.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves all movies for a given user from the database.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Adds a new user to the database.
        """
        pass

    @abstractmethod
    def add_movie(self, movie, user_id, rating):
        """
        Adds a new movie to the database.
        """
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, rating):
        """
        Updates an existing movie in the database.
        """
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """
        Deletes a movie from the database.
        """
        pass
