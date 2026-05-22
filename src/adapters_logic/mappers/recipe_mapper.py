import ast
from typing import List, Optional
from ..dtos.recipe_dto import RecipeDTO
from src.alchemy_db.models.recipes_model import Recipe  # adjust path

def parse_string_list(raw_str: str) -> List[str]:
    if not raw_str:
        return []
    try:
        return ast.literal_eval(raw_str)
    except (ValueError, SyntaxError):
        return []

def stringify_list(lst: list) -> str:
    return str(lst) if lst else "[]"


def recipe_to_dto(recipe: Recipe) -> RecipeDTO:
    return RecipeDTO(
        recipe_id=recipe.recipe_id,
        name=recipe.name,
        description=recipe.description,
        ingredients=parse_string_list(recipe.ingredients_raw_str),
        serving_size_grams=recipe.serving_size_grams,
        servings=recipe.servings,
        steps=parse_string_list(recipe.steps)
    )


def dto_to_recipe(dto: RecipeDTO, recipe: Optional[Recipe] = None) -> Recipe:
    if recipe is None:
        recipe = Recipe()

    recipe.name = dto.name
    recipe.description = dto.description
    recipe.ingredients_raw_str = stringify_list(dto.ingredients)
    recipe.serving_size_grams = dto.serving_size_grams
    recipe.servings = dto.servings
    recipe.steps = stringify_list(dto.steps)

    return recipe