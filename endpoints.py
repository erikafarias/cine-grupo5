import requests

url: str = 'http://vps-3701198-x.dattaweb.com:4000'
token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
auth: dict = {'Authorization': f'Bearer {token}'}

r = requests.get(url, headers=auth)

#TODO: PROBAR get_movies_by_id Y get_cinemas_by_movie_id
#TODO: DEFINIR CÓMO PASAR RESPUESTA Y EXCEPCIONES

def get_movies() -> dict:
    endpoint_url: str = f'{url}/movies'
    response = requests.get(endpoint_url, headers=auth)
    print(response.raise_for_status())
    movies: list[dict] = response.json()
    print(movies)

    return movies


def get_movies_by_id(id: str) -> dict:
    endpoint_url: str = f'{url}/movies/{id}'
    response = requests.get(endpoint_url, headers=auth)
    response.raise_for_status()
    movie: dict = response.json()
    # if response.status_code == 400:
    #     message: str = 'No se encontró la película seleccionada'
    #     movie: dict = {}
    # elif response.status_code == 500:
    #     message: str = 'No se pudo hacer la consulta, intente nuevamente más tarde'
    #     movie: dict = {}
    # elif response.status_code == 200:
    #     message: str = 'OK'
    #     movie: dict = response.json()

    return movie


def get_cinemas_by_movie_id(id: str) -> dict:
    endpoint_url: str = f'{url}/movies/{id}/cinemas'
    response = requests.get(endpoint_url, headers=auth)
    response.raise_for_status()
    cinemas: dict = response.json()
    return cinemas

# get_movies()
