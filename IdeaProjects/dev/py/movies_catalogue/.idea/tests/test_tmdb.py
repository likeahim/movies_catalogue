import tmdb_client
from unittest.mock import Mock

def test_get_poster_url_uses_default_size():
    # Przygotowanie danych
    poster_api_path = "some-poster-path"
    expected_default_size = 'w342'
    # Wywołanie kodu, który testujemy
    poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
    # Porównanie wyników
    assert expected_default_size in poster_url

def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list is not None

def some_function_to_mock():
    raise Exception("Original was called")

def test_mocking(monkeypatch):
    my_mock = Mock()
    my_mock.return_value = 2
    monkeypatch.setattr("tests.test_tmdb.some_function_to_mock", my_mock)
    result = some_function_to_mock()
    assert result == 2

def test_get_movies_list(monkeypatch):
    # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
    mock_movies_list = ['Movie 1', 'Movie 2']

    requests_mock = Mock()
    # Wynik wywołania zapytania do API
    response = requests_mock.return_value
    # Przysłaniamy wynik wywołania metody .json()
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list

def test_get_single_movie(monkeypatch):
    mock_movie = "Movie 1"
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movie
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie = tmdb_client.get_single_movie(1)
    assert movie == mock_movie

def test_get_single_movie_cast(monkeypatch):
    mock_cast = ["Robert DeNiro", "Al Pacino"]
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_cast
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    cast = tmdb_client.get_single_movie_cast(f"{1}/credits")
    assert cast == mock_cast