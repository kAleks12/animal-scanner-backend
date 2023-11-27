from functools import lru_cache

import requests

from src.server.model.data.search import PlaceDTO, PositionDTO


@lru_cache(maxsize=10000)
def get_search_results(query: str) -> list[PlaceDTO]:
    params = {'q': query, 'format': 'json'}
    response = requests.get(" https://nominatim.openstreetmap.org/search", params=params)
    data = response.json()
    output = []
    for place in data:
        name = place["display_name"]
        x = place["lat"]
        y = place["lon"]
        position = PositionDTO(x=x, y=y)
        entry = PlaceDTO(value=position, label=name)
        output.append(entry)
    return output
