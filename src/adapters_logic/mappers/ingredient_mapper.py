from typing import Optional

from src.adapters_logic.dtos.ingredient_dto import IngredientDTO
from src.alchemy_db.models.ingredients_model import Ingredient


def ingredient_to_dto(
    ingredient: Ingredient
) -> IngredientDTO:
    return IngredientDTO(
        ingredient_id=ingredient.ingredient_id,
        name=ingredient.name,
    )


def dto_to_ingredient(
    dto: IngredientDTO,
    ingredient: Optional[Ingredient] = None
) -> Ingredient:

    if ingredient is None:
        ingredient = Ingredient()

    ingredient.name = dto.name

    return ingredient