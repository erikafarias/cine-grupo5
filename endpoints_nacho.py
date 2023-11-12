import requests

url: str = "http://vps-3701198-x.dattaweb.com:4000"
token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
authorization: dict = {'Authorization': f'Bearer {token}'}


def stock_snacks() -> list:
    ''''
    Post: Devuelve una lista de diccionarios con cada snack disponible (Stock infinito)
    '''

    endpoint: str = f'{url}/snacks'
    response = requests.get(endpoint, headers=authorization)
    response.raise_for_status()

    stock_of_snacks: list[dict] = response.json()

    return stock_of_snacks
