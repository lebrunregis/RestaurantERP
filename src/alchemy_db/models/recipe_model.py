from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base_model import Base


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=False,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(501),
        unique=False,
        nullable=True
    )
    ingredients_raw_str: Mapped[str] = mapped_column(
        String(502),
        unique=False,
        nullable=False
    )
    serving_size: Mapped[str] = mapped_column(
        String(53),
        unique=False,
        nullable=False
    )
    servings: Mapped[int] = mapped_column(
        unique=False,
        nullable=False
    )
    steps: Mapped[str] = mapped_column(
        String(500),
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return f'Recipe : ID : {self.recipe_id} USERNAME : {self.name}'