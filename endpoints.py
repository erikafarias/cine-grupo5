import requests


TOKEN:str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
AUTH:dict = {'Authorization': f'Bearer {TOKEN}'}
URL:str = 'http://vps-3701198-x.dattaweb.com:4000'


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
    