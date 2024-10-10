import requests
from bs4 import BeautifulSoup

from .objectMovies import Movie


def parse_moveis() -> list[Movie]:
    _STATUS_CODE: int = 200
    
    response = requests.get("https://likefilmdb.ru/service/movies/best/")
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != _STATUS_CODE:
        return []

    movies: list[Movie] = []

    for item in soup.find_all('div', class_="uiMovieListSimpleSection"):
        for movie in item.find_all("div", class_="uiMovieVarXVWrapper"):
            string_title: str = movie.find("div", class_="uiMovieVarXVTitle").text
            string_rating: str = movie.find("td", class_="uiStandartVarListVal").text
            
            description: str = movie.find("div", class_="uiMovieVarXVContent").p.text
            title: str = string_title[:string_title.find('(')]
            rating: float = float(string_rating.split(' ')[-1])

            movies.append(Movie(title, description, rating))

    return movies
