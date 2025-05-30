# MovieWeb App: A Flask Movie Web Application

<img width="573" alt="Screenshot 2025-04-11 at 21 25 33" src="https://github.com/user-attachments/assets/e87f8826-2974-4d76-a9a7-c0586aadf41c" />

## About this Project

This program is a learning project for the Software Engineering
Bootcamp at MasterSchool. It showcases what I have learned
about Python programming, API and web development.
A step-by-step guide is included to help you understand how the
code has been implemented.

Now with deployment on https://veronicalobos.pythonanywhere.com/ !

## Technologies Used

<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" title="Python"/><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/html.png" alt="HTML" title="HTML"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/css.png" alt="CSS" title="CSS"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/pycharm.png" alt="PyCharm" title="PyCharm"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/flask.png" alt="Flask" title="Flask"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/sqlite.png" alt="SQLite" title="SQLite"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/rest.png" alt="REST" title="REST"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/postman.png" alt="Postman" title="Postman"/>


## Features

Two versions of the MovieWeb App are provided:
1. **app_csr.py**: This version is an API. Clients can implement
their own front-end using the provided endpoints. It is a 
Client-Side Rendering (CSR) version.
Can be tested using Postman or any other API testing tool.
2. **app_ssr.py**: This version is a Restful API with Server-Side 
Rendering (SSR) using Flask and Jinja2 templates.
It has been deployed on PythonAnywhere.

 - CRUD operations for managing movies, users and ratings.
 - The API is built using Flask and SQLAlchemy, and it uses
    SQLite as the database.
 - Endpoints for adding, updating, and deleting movies, adding
    users, and retrieving movie details.
 - Input validation in templates to ensure that the user
    provides valid data before submitting the form.
 - Deletion confirmation for movies and users to prevent
    accidental deletions.
 - Redirection (with Javascript) to the home page after deleting
    a movie.
 - The API fetches movie data from the OMDb API using the
    omdb_data_fetcher module (requires an API key).
 - SSR (Server-Side Rendering) is used to render HTML jinja2
    templates for the web application, and a stylesheet
    (style.css) with a responsive minimalist design is included.
 - The app is designed to be user-friendly and easy to navigate,
    with a simple and intuitive interface.
 - DAL (Data Access Layer) is implemented using SQLAlchemy ORM
    with SQLite, through the DataManagerSQLite class, for
    managing database operations.
 - OOP (Object-Oriented Programming) is used to define the
    User and Movie classes, which represent the database tables.
 - The app is designed to be modular and easy to extend
    with additional features in the future.
 - Logging is implemented to track operations where a user ID
    is involved, such as adding or deleting movies.

## Directory Structure

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
│   ├── about.html
│   ├── add_movie.html
│   ├── add_user.html
│   ├── delete_movie.html
│   ├── home.html
│   ├── movie_info.html
│   ├── redirect.html
│   ├── update_movie.html
│   ├── user_movies.html
│   └── users.html
├── .env  >>> my_api_key="..." * your api key goes here *
├── app_csr.py
├── app_ssr.py
├── data_models.py
├── omdb_data_fetcher.py
├── README.md  * you are here *
└── requirements.txt
```

## User Guide

These are the steps to run the MovieWeb App locally.  

### 1. Setting Up the Environment

* Set up a virtual environment (the app uses Python 3.9):
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
* Install the required packages with pip or your preferred package manager:  
```bash
pip install -r requirements.txt
```

### 2. Clone the Repository
```bash
git clone https://github.com/VeronicaLobos/MoviWeb-App.git
cd MovieWeb-App
```

### 3. Set Up the Environment Variables
The app uses an API key to fetch movie data from the OMDb API. You will need to register at https://www.omdbapi.com to obtain one.
Create a `.env` file in the root directory of the project and add the API Key to the `.env` file like this:
```plaintext
my_api_key="YOUR_OMDB_API_KEY"
```
Without this key, the app will not be able to fetch movie data from the OMDb API.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
* To run the CSR version of the app:
```bash
python app_ssr.py
```
* To run the SSR version of the app:
```bash
python app_csr.py
```

### 6. Access the Application
Open your web browser and go to ```localhost:5002/home```


## Sneak peek

<img width="573" alt="Screenshot 2025-04-11 at 21 25 51" src="https://github.com/user-attachments/assets/19a08bce-f22d-45c1-8be6-4901448fb8c3" />

<img width="573" alt="Screenshot 2025-04-17 at 11 56 56" src="https://github.com/user-attachments/assets/8c22880c-4aec-44c4-b2fb-d551c631dac4" />

<img width="573" alt="Screenshot 2025-04-17 at 11 57 56" src="https://github.com/user-attachments/assets/21e72d15-8c8f-4e9a-a701-3c05325f35fa" />
