import requests
from bs4 import BeautifulSoup


def parser_site() -> list[dict[str, str | float]]:
    response = requests.get("https://likefilmdb.ru/service/movies/best/")
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        return []

    movies: list[dict[str, str | float]] = []

    for item in soup.find_all('div', class_="uiMovieListSimpleSection"):
        for movie in item.find_all("div", class_="uiMovieVarXVWrapper"):
            string_title: str = movie.find("div", class_="uiMovieVarXVTitle").text
            string_rating: str = movie.find("td", class_="uiStandartVarListVal").text
            
            description: str = movie.find("div", class_="uiMovieVarXVContent").p.text
            title: str = string_title[:string_title.find('(')]
            rating: float = float(string_rating.split(' ')[-1])

            movies.append({
                "title": title,
                "description": description,
                "rating": rating
            })

    return movies

