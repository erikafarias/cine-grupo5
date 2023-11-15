import requests

URL:str = 'http://vps-3701198-x.dattaweb.com:4000'
TOKEN:str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
AUTH:dict = {'Authorization': f'Bearer {TOKEN}'}
   

def get_movies() -> list[dict]:
    movies: list[dict] = []
    try:
        endpoint_url: str = f'{URL}/movies'
        response = requests.get(endpoint_url, headers=AUTH)
        print(response.raise_for_status())
        movies = response.json()
        print(movies)
    except requests.exceptions.HTTPError as http_err:
        print(f'Ocurrió un error: {http_err}. Código: {response.status_code}')

    return movies


def get_movie_by_id(id: int) -> dict:
    movie: dict = {}
    try:
        endpoint_url: str = f'{URL}/movies/{id}'
        response = requests.get(endpoint_url, headers=AUTH)
        print(response.raise_for_status())
        movie: dict = response.json()
        print(movie)
    except requests.exceptions.HTTPError as err:
        print(f'Ocurrió un error: {err}. Código: {response.status_code}')
    return movie


def get_cinemas_by_movie_id(id: int) -> list[str]:
    cinemas: list[str] = []
    try:
        endpoint_url: str = f'{URL}/movies/{id}/cinemas'
        response = requests.get(endpoint_url, headers=AUTH)
        response.raise_for_status()
        cinemas = response.json()
        print(cinemas)
    except requests.exceptions.HTTPError as err:
        print(f'Ocurrió un error: {err}. Código: {response.status_code}')
    return cinemas

  
def get_cinemas() -> list[dict]:
    
    '''
    Obtener información de todos los cines.
    '''
    
    endpoint:str = f'{URL}/cinemas'
    
    try:
        response = requests.get(endpoint, headers = AUTH)
        response.raise_for_status()
        
        cinemas:list[dict] = response.json()
        return cinemas
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))


def get_movies_by_cinema(cinema_id:int) -> list[dict]:
    
    '''
    Obtener películas proyectadas en un determinado cine.
    '''
    
    endpoint:str = f'{URL}/cinemas/{cinema_id}/movies'
    
    try:
        response = requests.get(endpoint, headers = AUTH)
        response.raise_for_status()
    
        movies_by_cinema:list[dict] = response.json()
        return movies_by_cinema
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))
        
        