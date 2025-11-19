import requests
import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environmental variables from .env file
load_dotenv()

class MovieAPIClient:
    BASE_URL = os.getenv("TMDB_BASE_URL")
    API_KEY = os.getenv("TMDB_API_KEY")

    def __init__(self):
        if not self.API_KEY:
            raise ValueError("TMDB_API_KEY environmental variable value not set. Please check your .env file.")
        
        self.headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "accept": "application/json"
        }
    
    @lru_cache(maxsize=128)
    def get_movie_details(self, movie_id:int) -> dict|None:

        endpoint = f"{self.BASE_URL}/movie/{movie_id}"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()

            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error fetching movie ID {movie_id} : {e} ")
            if response.status_code == 404:
                return None
            return {"error": f"API error : {response.status_code}", "message": response.json().get("status_message", "Unknown API error")}
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed for movie ID {movie_id} : {e}")
            return {"error":"Network or Connection error", "message": str(e)}
        
    @lru_cache(maxsize=32)
    def search_movies(self, query:str) -> dict|None:

        endpoint = f"{self.BASE_URL}/search/movie"
        params = {"query" : query}

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error searching for '{query}': {e}")
            return {"error": f"API Error: {response.status_code}", "message": response.json().get('status_message', 'Unknown API error')}
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed searching for '{query}': {e}")
            return {"error": "Network or connection error", "message": str(e)}    