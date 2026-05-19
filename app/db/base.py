from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic can detect them.
from app.models import Category, Game, Mechanic, Rating  # noqa: E402, F401
   