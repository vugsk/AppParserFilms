from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: str
    rating: float


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    class Config:
        from_attributes: bool = True
        