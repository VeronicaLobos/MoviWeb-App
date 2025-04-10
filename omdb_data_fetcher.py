"""
A module for extracting movie data from OMDb API,
The Open Movie Database https://www.omdbapi.com/
a RESTful web service to obtain movie information.
"""

import os
import json
import requests as req
from dotenv import load_dotenv
import urllib3.exceptions
from data_models import Movie


def _get_movie_info(movie_name: str) -> dict:
    """
    Fetches movie information from the OMDb API based
    on the provided movie title.

    This function makes a request to the OMDb API using
    the given movie title and your API key.
    It parses the JSON response into a Python dictionary
    containing movie attributes.

    :param movie_name: The title of the movie to look for.
    Returns a dictionary containing movie attributes if
    found, or an empty dictionary if not found or an
    error occurs.
    """
    load_dotenv()
    api_key = os.getenv("my_api_key")
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

    try:
        response = req.get(url)
        response.raise_for_status() # handle bad responses
        print(f"Requesting '{movie_name}' to {url}")
        json_string = response.text
        movie_info_dict = json.loads(json_string)
        if "Movie not found!" in json_string:
            print(json_string)
            return {}

        return movie_info_dict

    except NameError as e:
        print(f"Error: {e}")
        print("Check URL and API key and try again.")
    except KeyError as e:
        print(f"Key Error: {e}")
        print("Check if the API key 'my_api_key' is set "
              "in your environment variables.")
    except req.exceptions.Timeout:
        print(f"Request timed out after 10 seconds for '{movie_name}'.")
    except req.exceptions.ConnectionError as e:
        if isinstance(e.args[0], urllib3.exceptions.NameResolutionError):
            print(f"Name Resolution Error: {e}")
        else:
            print(f"Connection Error: {e}")
        print(e)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
    except (req.exceptions.HTTPError,
            req.exceptions.RequestException) as e:
        print(f"HTTP Error: {e}")
    return {}


def get_new_movie_data(movie_name):
    """
    Fetches and formats movie data from the OMDb API.

    - This function takes a movie title, fetches movie
    information using _get_movie_info(), extracts the
    year, director, genre, and poster URL.
    - If the title contains spaces, replaces them with
    "+".

    Returns a Movie object containing the attributes
    of the movie extracted from the dictionary obtained
    from the API.
    Returns None if any error occurs, or if the movie
    data is not found in the API.
    """
    movie_name = movie_name.replace(" ", "+")
    movie_info = _get_movie_info(movie_name)

    if movie_info != {}:
        try:
            new_movie_obj = Movie(
                movie_name = str(movie_info.get("Title")),
                year = int(movie_info.get("Year")),
                director = str(movie_info.get("Director")),
                genre=str(movie_info.get("Genre")),
                poster_url = str(movie_info.get("Poster"))
            )
            return new_movie_obj
        except TypeError as e:
            print(e)
        except UnboundLocalError as e:
            print(e)

    return None

if __name__ == "__main__":
    # Example usage
    movie_title = "The Shawshank Redemption"
    movie_data = get_new_movie_data(movie_title)
    if movie_data:
        print(f"Movie Name: {movie_data.movie_name}")
        print(f"Year: {movie_data.year}")
        print(f"Director: {movie_data.director}")
        print(f"Genre: {movie_data.genre}")
        print(f"Poster URL: {movie_data.poster_url}")
    else:
        print("Movie not found.")