import requests
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYzI0OTY0YWUyZGIxYmVlMTNlNTdmOGQ3MWUyZjQ4MiIsIm5iZiI6MTc0MzY5NDEzOC43NTUsInN1YiI6IjY3ZWVhOTNhNDY4MGYyNmJmM2E3YmIyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.djSoWLofNeseWi-7z4ILwigetR0NyQf_FMPXPGStLtQ"

def get_movies_list(list_type="popular"):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_movies(how_many, list_type="popular"):
    data = get_movies_list(list_type)
    return data["results"][:how_many]

def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()["cast"]