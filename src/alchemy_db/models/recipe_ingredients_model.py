from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from .base_model import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.recipe_id"),primary_key=True, )
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.ingredient_id"),primary_key=True )
    
    recipe = relationship("Recipe", back_populates="ingredient_links")
    ingredient = relationship("Ingredient", back_populates="supplier_links")