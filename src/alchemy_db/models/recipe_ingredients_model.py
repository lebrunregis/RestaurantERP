from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index

from .base_model import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.recipe_id", ondelete="CASCADE"), 
        primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.ingredient_id", ondelete="CASCADE"), 
        primary_key=True
    )

    recipe_links = relationship(
        "Recipe", 
        back_populates="ingredient_links",
        single_parent=True, 
        cascade="all, delete-orphan"
    )
    ingredient_links = relationship(
        "Ingredient",
        single_parent=True, 
        back_populates="recipe_ingredient_links"
    )

    # Add index to speed up queries grouped by ingredient_id
    __table_args__ = (
        Index("ix_recipe_ingredients_ingredient_id", "ingredient_id"),
        Index("ix_recipe_ingredients_recipe_id", "recipe_id"),
    )