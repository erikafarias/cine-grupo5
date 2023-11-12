import requests

TOKEN:str = '' # completar con el token de la API
AUTHORIZATION:str = 'Bearer ' + TOKEN
URL:str = 'http://vps-3701198-x.dattaweb.com:4000'

def get_cinemas(token:str) -> dict:
    
    '''
    Obtener información de todos los cines.
    '''
    
    endpoint:str = f'{URL}/cinemas'
    
    try:
        response = requests.get(endpoint, headers={'Authorization': AUTHORIZATION })
        response.raise_for_status()
        
        cinemas:dict = response.json()
        return cinemas
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))


def get_movies_by_cinema(token:str, cinema_id:int) -> dict:
    
    '''
    Obtener películas proyectadas en un determinado cine.
    '''
    
    endpoint:str = f'{URL}/cinemas/{cinema_id}/movies'
    
    try:
        response = requests.get(endpoint, headers={'Authorization': AUTHORIZATION })
        response.raise_for_status()
    
        movies_by_cinema:dict = response.json()
        return movies_by_cinema
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))
    
