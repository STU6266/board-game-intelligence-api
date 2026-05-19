from app.models.association_tables import game_categories, game_mechanics
from app.models.category import Category
from app.models.game import Game
from app.models.mechanic import Mechanic
from app.models.rating import Rating

__all__ = [
    "Game",
    "Rating",
    "Category",
    "Mechanic",
    "game_categories",
    "game_mechanics",
]
