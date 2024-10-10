from sqlalchemy.orm import Session

from . import models, schemas


def get_movies(db: Session, skip: int = 0):
    return db.query(models.MovieBase).offset(skip).all()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.MovieBase(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_movies_sorted_by_rating(db: Session, skip: int = 0):
    return db.query(models.MovieBase).order_by(models.MovieBase.rating.desc()).offset(skip).all()
