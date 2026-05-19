from sqlalchemy import Column, ForeignKey, Table

from app.db.base import Base


game_categories = Table(
    "game_categories",
    Base.metadata,
    Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


game_mechanics = Table(
    "game_mechanics",
    Base.metadata,
    Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
    Column("mechanic_id", ForeignKey("mechanics.id", ondelete="CASCADE"), primary_key=True),
)
