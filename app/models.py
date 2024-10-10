from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class MovieBase(Base):
    __tablename__ = "films"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    