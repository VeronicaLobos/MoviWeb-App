# MovieWeb App: A Flask Movie Web Application

## About this Project

This is a Restful API for a Movie Web App that allows users to
manage a list with their favorite movies and give a rating to
each movie, as well as retrieve movie details from the OMDb API
and edit the movie information.

This program is a learning project for the Software Engineering
Bootcamp at MasterSchool. It showcases what I have learned
about Python programming, API and web development.
A step-by-step guide is included to help you understand how the
code has been implemented.

## Features

 - Restful API architecture with CRUD operations for managing
    movies and users.
 - The API is built using Flask and SQLAlchemy, and it uses
    SQLite as the database.
 - Endpoints for adding, updating, and deleting movies, adding
    users, adding user ratings, and retrieving movie details
    and user ratings.
 - Input validation in templates to ensure that the user
    provides valid data before submitting the form.
 - The API also fetches movie data from the OMDb API using the
    omdb_data_fetcher module (requires an API key).
 - SSR (Server-Side Rendering) is used to render HTML jinja2
    templates for the web application, and a stylesheet
    (style.css) with a responsive minimalist design is included.
 - DAL (Data Access Layer) is implemented using SQLAlchemy ORM
    with SQLite, through the DataManagerSQLite class, for
    managing database operations.
 - OOP (Object-Oriented Programming) is used to define the
    User and Movie classes, which represent the database tables.
 - The app is designed to be modular and easy to extend
    with additional features in the future.


```plaintext
MovieWeb-App/
├── .idea/
├── static/
│   └── style.css
├── datamanager/
│   ├── __init__.py
│   ├── data_manager_interface.py
│   ├── data_manager_sqlite.py
├── templates/
│   ├── add_movie.html
│   ├── add_user.html
│   ├── home.html
│   ├── movie_info.html
│   ├── redirect.html
│   ├── update_movie.html
│   ├── update_rating.html
│   ├── user_movies.html
│   └── users.html
├── .env  >>> my_api_key="..."
├── app.py
├── data_models.py
├── omdb_data_fetcher.py
├── README.md  * you are here *
└── requirements.txt
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

