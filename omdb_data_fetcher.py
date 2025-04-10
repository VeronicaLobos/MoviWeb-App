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
import time

from data_models import Movie


def _get_movie_info(movie_name: str, max_retries=3, initial_delay=1) -> dict:
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
    retries = 0

    while retries < max_retries:
        try:
            response = req.get(url)
            response.raise_for_status()
            print(f"Requesting '{movie_name}' to {url} (Attempt {retries + 1})")
            json_string = response.text
            movie_info_dict = json.loads(json_string)
            if "Movie not found!" in json_string:
                print(json_string)
                return {}
            return movie_info_dict
        except req.exceptions.HTTPError as e:
            if response is not None and response.status_code == 500:
                retries += 1
                delay = initial_delay * (2 ** (retries - 1))  # Exponential backoff
                print(f"OMDb API Server Error (500) for '{movie_name}'. "
                      f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"HTTP Error for '{movie_name}': {e}")
                break
        except req.exceptions.ConnectionError as e:
            if isinstance(e.args[0], urllib3.exceptions.NameResolutionError):
                print(f"Name Resolution Error: Could not resolve the address for OMDb API. "
                      f"Please check your internet connection.")
            else:
                print(f"Connection Error: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            break
        except req.exceptions.Timeout:
            print(f"Request timed out after 10 seconds for '{movie_name}'.")
            break
        except req.exceptions.RequestException as e:
            print(f"General Request Error: {e}")
            break

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
            print(f"Type Error while creating Movie object: {e}")
        except UnboundLocalError as e:
            print(f"UnboundLocalError while creating Movie object: {e}")

    if movie_info == {}:
        print("Could not fetch the movie data")
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
