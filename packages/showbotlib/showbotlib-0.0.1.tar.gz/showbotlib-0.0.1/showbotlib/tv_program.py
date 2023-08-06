import requests
import sys
import time
import pickle
from pathlib import Path
from pydantic import BaseModel, validator


class Country(BaseModel):
    name: str

    @validator("name")
    def check_empty(cls, v):
        if v == "":
            raise ValueError("No data")
        return v


class Network(BaseModel):
    name: str
    country: Country

    @validator("name")
    def check_empty(cls, v):
        if v == "":
            raise ValueError("No data")
        return v


class TVShow(BaseModel):
    name: str
    network: Network
    summary: str

    @validator("name", "summary")
    def check_empty(cls, v):
        if v == "":
            raise ValueError("No data")
        return v


class Cache:
    def __init__(self, ttl: int = 120):
        self.ttl = ttl
        self.folder = Path("cache")
        if not self.folder.exists():
            self.folder.mkdir()

    def __getitem__(self, item):
        path = Path(self.folder, item)

        if path.exists():
            tl_file = int(time.time() - path.stat().st_mtime)
            if tl_file < self.ttl:
                with path.open("rb") as f:
                    return pickle.load(f)
        raise ValueError("Data not exists or outdated")

    def __setitem__(self, item, value):
        path = Path(self.folder, item)
        with path.open("wb") as f:
            pickle.dump(value, f)


def cache_it(sec: int = 120):
    cache = Cache(sec)

    def _cache_it(func):
        def wrap(search_film_name):
            data = {}
            try:
                data = cache[search_film_name]
            except ValueError:
                data = func(search_film_name)
                cache[search_film_name] = data
            return data

        return wrap

    return _cache_it


@cache_it(120)
def get_show_data(search_film_name: str):
    search_url = "https://api.tvmaze.com/singlesearch/shows?q="
    search_req = search_url + search_film_name
    request_api = requests.get(search_req)
    if request_api.status_code != 200:
        if request_api.status_code == 404:
            raise ValueError("Show not found")
        else:
            raise RuntimeError("Error request")

    show_data = TVShow.parse_raw(request_api.text)

    return show_data


if __name__ == "__main__":
    search_film_name = "\\ ".join(sys.argv[1:])

    try:
        show_data = get_show_data(search_film_name)
        print(f"Name: {show_data.name}")
        print(f"Network Name: {show_data.network.name}")
        print(f"Network Country Name: {show_data.network.country.name}")
        print(f"Summary: {show_data.summary}")
    except ValueError as e:
        print(e)
