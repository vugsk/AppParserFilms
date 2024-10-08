import requests
from bs4 import BeautifulSoup


def te(i: str) -> str:
    if i.rfind('+') != -1:
        return i[:i.rfind('+') - 3]
    return i


def parser_site(url: str) -> list[dict[str, str | int | float]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if response.status_code != 200:
        return []
    
    movies: list[dict[str, str | int | float]] = []
    
    for item in soup.find_all('div', class_="redesign_afisha_movies"):
        for film in item.find_all("div", class_="redesign_afisha_movie_main"):
            string_name_and_year = film.find("div", class_="redesign_afisha_movie_main_subtitle")
            string_rating = film.find("div", class_="redesign_afisha_movie_main_rating")
            
            string_not_spaces: str = ' '.join(te(' '.join(string_name_and_year.text.split())).split())
            
            name: str = string_not_spaces[:string_not_spaces.rfind(' ')]
            year: int = int(string_not_spaces.split(' ')[-1])
            rating: float = float(string_rating.find_all("div")[2].text.split(' ')[-1])
            
            movies.append({
                "title": name,
                "year": year,
                "rating": rating
            })
            
    return movies


def parser_page_with_site(url: str, count_page: int) -> list[dict[str, str | int | float]]:
    movies: list[dict[str, str | int | float]] = []
    for i in range(0, count_page):
        for j in parser_site(url + str(i)):
            movies.append(j)
    return movies


print(len(parser_page_with_site(
    "https://www.film.ru/compilation/100-velichayshih-filmov-po-versii-chitateley-empire/page/",
        4)))
