import requests

url: str = 'http://vps-3701198-x.dattaweb.com:4000'
token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
auth: dict = {'Authorization': f'Bearer {token}'}


def get_movies() -> list[dict]:
    movies: list[dict] = []
    try:
        endpoint_url: str = f'{url}/movies'
        response = requests.get(endpoint_url, headers=auth)
        print(response.raise_for_status())
        movies = response.json()
        print(movies)
    except requests.exceptions.HTTPError as http_err:
        print(f'Ocurrió un error: {http_err}. Código: {response.status_code}')

    return movies


def get_movie_by_id(id: int) -> dict:
    movie: dict = {}
    try:
        endpoint_url: str = f'{url}/movies/{id}'
        response = requests.get(endpoint_url, headers=auth)
        print(response.raise_for_status())
        movie: dict = response.json()
        print(movie)
    except requests.exceptions.HTTPError as err:
        print(f'Ocurrió un error: {err}. Código: {response.status_code}')
    return movie


def get_cinemas_by_movie_id(id: int) -> list[str]:
    cinemas: list[str] = []
    try:
        endpoint_url: str = f'{url}/movies/{id}/cinemas'
        response = requests.get(endpoint_url, headers=auth)
        response.raise_for_status()
        cinemas = response.json()
        print(cinemas)
    except requests.exceptions.HTTPError as err:
        print(f'Ocurrió un error: {err}. Código: {response.status_code}')
    return cinemas


#get_movies()
get_movie_by_id(1)
get_movie_by_id(30)
get_cinemas_by_movie_id(1)
get_cinemas_by_movie_id(30)
