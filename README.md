# MovieWeb App: A Flask Movie Web Application

## About this Project

This is a simple Flask application that uses SQLAlchemy to manage a movie database. Currently, a Work in Progress.

## Core Functionalities

_User Selection:_ The ability for a user to select their identity from a list of users.  

_Movie Management:_ After a user is selected, the application will display a list of their favorite movies. From here, users should be able to:  

- Add a new movie: Movie's name, director, year of release, and rating.  
- Delete a movie: Remove a movie from the user's list.  
- Update a movie: Modify the details of an existing movie from the user's list.  
- List all movies: Display all movies in the user's list.  

_Data Source Management:_ Use a Python class to manage the data source.

## Application Structure

Key parts of the application:  
- _User Interface (UI):_ An intuitive web interface built using Flask, HTML, and CSS. It will provide forms for adding, updating, and deleting movies, as well as a method to select a user.  
- _A Python class:_ To handle operations related to the data source. This class exposes functions for getting all users, getting a user’s movies, and updating a user’s movie.  
- _A database (SQLite):_ For storing user and movie data. The database will be created and managed using SQLAlchemy, an ORM for Python.

```plaintext
MovieWeb-App/
├── requirements.txt
README.md <!-- This file -->
```

### Classes for Database Management

Class for Database Management Interface and Implementation:

* _DataManagerInterface(ABC) class:_  
This is an abstract base class that defines the interface for the DataManager using Pythons ```abc``` module. The DataManager interface specifies a few methods that must be implemented by any concrete DataManager class. The methods include:
  - get_all_users(), abstract method
  - get_user_movies(user_id), abstract method
  - add_movie(user_id, movie)
  - delete_movie(user_id, movie_id)
  - update_movie(user_id, movie_id, updated_movie)<br>   

* _DataManager class (SQLite):_  
This class implements the DataManagerInterface and provides concrete implementations for the methods defined in the interface. It uses SQLAlchemy to interact with the SQLite database. The class inherits from the DataManagerInterface and implements the methods to manage the database. The class also includes a constructor that initializes the database connection and creates the tables if they do not exist.

Database Models are defined using SQLAlchemy ORM. The User and Movie classes represent the database tables.

* _User class:_ Each User instance will have:  
  - a unique ID (id), Primary Key  
  - the user's name (name)  

* _Movie class:_ Each Movie instance will have:  
  - a unique ID (id), Primary Key  
  - a movie name (name)  
  - a director's name (director)  
  - a year of release (year)  
  - a rating (rating) 


## User Guide

These are the steps to run the MovieWeb App locally.  

### 1. Setting Up the Environment

* Set up a virtual environment:  
```bash
python -m venv venv
```
* Activate the virtual environment:  
```bash
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```
* Install the required packages:  
```bash
pip install -r requirements.txt
```

### 2. Clone the Repository
```bash
git clone https://github.com/VeronicaLobos/MoviWeb-App.git
cd MovieWeb-App
```

