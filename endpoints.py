import requests

token:str = '' # completar con el token de la API

def getCinemas(token:str) -> dict:
    
    '''
    Obtener información de todos los cines.
    '''
    
    url:str = 'http://vps-3701198-x.dattaweb.com:4000/cinemas'
    authorization:str = "Bearer " + token
    
    try:
        response = requests.get(url, headers={'Authorization': authorization })
        response.raise_for_status()
        
        cinemas:dict = response.json()
        return cinemas
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))


def getMoviesByCinema(token:str, cinemaId:int) -> dict:
    
    '''
    Obtener películas proyectadas en un determinado cine.
    '''
    
    url:str = 'http://vps-3701198-x.dattaweb.com:4000/cinemas/' + str(cinemaId) + '/movies'
    authorization:str = "Bearer " + token
    
    try:
        response = requests.get(url, headers={'Authorization': authorization })
        response.raise_for_status()
    
        moviesByCinema:dict = response.json()
        return moviesByCinema
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit('ERROR: ' + str(err))
    
