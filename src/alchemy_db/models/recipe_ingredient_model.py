from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base_model import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        return f'Recipe : ID : {self.recipe_id} Ingredient : ID : {self.ingredient_id}'