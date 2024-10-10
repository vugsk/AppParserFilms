from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas, parser, objectMovies
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates/")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def equal(list1, list2: list[models.MovieBase]) -> list[objectMovies.Movie]:
    if len(list1) == 0:
        return list1
    
    exist_in_two_lists = [[i for j in list2 if i.title == j.title] for i in list1]
    
    are_number_of_elements_is_equal: bool = len(exist_in_two_lists) == len(list1)
    are_two_lists_equal: bool = len(list1) == len(list2)
    is_empty: bool = len(exist_in_two_lists) == 0
    
    if are_number_of_elements_is_equal and are_two_lists_equal:
        list1.clear()
    elif (not (are_number_of_elements_is_equal or are_two_lists_equal)) and not is_empty:
        for i in exist_in_two_lists:
            list1.remove(i)
    
    return list1


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    movies: list[models.MovieBase] = crud.get_movies_sorted_by_rating(db)
    
    render_page: str = "index.html"
    data: dict[str, Request | list[models.MovieBase]] = {
        "request": request,
        "movies": movies
    }
    
    return templates.TemplateResponse(render_page, data)


@app.post("/movies/load")
def load_movies(db: Session = Depends(get_db)):
    movies: list[objectMovies.Movie] = parser.parse_moveis()
    movies_database: list[models.MovieBase] = crud.get_movies(db)
    status: str = ""
    
    if len(movies_database) != 0 and (len(equal(movies, movies_database)) == 0):
        status = "OLD"
    else:
        status = "NEW"
        for movie in movies:
            crud.create_movie(db, schemas.MovieCreate(**movie.__dict__()))
        
    sorted_movies: list[models.MovieBase] = crud.get_movies_sorted_by_rating(db)
    
    return {
        "message": status,
        "content": [schemas.Movie.model_validate(movie).model_dump() for movie in sorted_movies]
    }
