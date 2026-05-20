from sqlalchemy.orm import Mapped, mapped_column, relationship
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
        String(500),
        unique=False,
        nullable=True
    )
    ingredients_raw_str: Mapped[str] = mapped_column(
        String(500),
        unique=False,
        nullable=False
    )
    serving_size_grams: Mapped[int] = mapped_column(
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

    ingredient_links = relationship("RecipeIngredient", back_populates="recipe_links", cascade="all, delete-orphan")