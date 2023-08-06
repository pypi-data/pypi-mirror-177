import requests

def unreleased():
    """Retorna los próximos talleres en codigofacilito

    >>> type(unreleased()) == type(dict())
    True
    """
    endpoint = 'https://codigofacilito.com/api/v2/workshops/unreleased'
    response = requests.get(endpoint)

    if response.status_code == 200:
        payload = response.json()
        return payload['data']

