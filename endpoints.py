import requests

URL: str = 'http://vps-3701198-x.dattaweb.com:4000'
TOKEN: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
AUTH: dict = {'Authorization': f'Bearer {TOKEN}'}
   

def get_movies() -> list[dict]:
    movies: list[dict] = []
    try:
        endpoint_url: str = f'{URL}/movies'
        response = requests.get(endpoint_url, headers=AUTH)
        response.raise_for_status()
        movies = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'Ocurrió un error: {http_err}. Código: {response.status_code}')

    return movies


def get_movie_by_id(id: str) -> dict:
    movie: dict = {}
    try:
        endpoint_url: str = f'{URL}/movies/{id}'
        response = requests.get(endpoint_url, headers=AUTH)
        response.raise_for_status()
        movie: dict = response.json()
    except requests.exceptions.HTTPError as err:
        print(f'Ocurrió un error: {err}. Código: {response.status_code}')
    return movie


def get_cinemas_by_movie_id(id: str) -> list[str]:
    cinemas: list[str] = []
    try:
        endpoint_url: str = f'{URL}/movies/{id}/cinemas'
        response = requests.get(endpoint_url, headers=AUTH)
        response.raise_for_status()
        cinemas = response.json()
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
        
        cinemas: list[dict] = response.json()
        return cinemas
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))


def get_movies_by_cinema(cinema_id: str) -> list[dict]:
    
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


def stock_snacks() -> tuple[list, list]:

        '''
        Los nombres y los precios por separado
        '''

        endpoint: str = f'{URL}/snacks'
        response = requests.get(endpoint, headers=AUTH)
        response.raise_for_status()

        stock_of_snacks: [dict] = response.json()
        list_names_snacks: list = []
        for elemento in stock_of_snacks:
            list_names_snacks.append(elemento)

        list_prices_snacks: list = []
        for elemento in list_names_snacks:
            list_prices_snacks.append(stock_of_snacks[elemento])

        return list_names_snacks, list_prices_snacks

def get_poster_by_id(id: str) -> dict:
    try:
        endpoint: str = f'{URL}/posters/{id}'
        response = requests.get(endpoint, headers=AUTH)
        response.raise_for_status()
        poster: dict = response.json()
        return poster
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))
        
