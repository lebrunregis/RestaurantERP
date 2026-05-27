import ast
import html
from typing import List, Optional
from ..dtos.recipe_dto import RecipeDTO
from src.alchemy_db.models.recipes_model import Recipe

# ---------- Helper Functions ----------
def parse_string_list(raw_str: str) -> List[str]:
    """Safely convert a string representation of a Python list into a real list, unescape HTML."""
    if not raw_str:
        return []
    try:
        lst = ast.literal_eval(raw_str)
        # Unescape all string elements
        return [html.unescape(str(item)) for item in lst]
    except (ValueError, SyntaxError):
        return []

def stringify_list(lst: list) -> str:
    """Convert a Python list to a string for DB storage"""
    return str(lst) if lst else "[]"

def recipe_to_dto(recipe: Recipe) -> RecipeDTO:
    """Map a SQLAlchemy Recipe model to a presentation-ready RecipeDTO with HTML unescaping"""
    return RecipeDTO(
        recipe_id=recipe.recipe_id,
        name=html.unescape(recipe.name),
        description=html.unescape(recipe.description) if recipe.description else "",
        ingredients=parse_string_list(recipe.ingredients_raw_str),
        serving_size_grams=recipe.serving_size_grams,
        servings=recipe.servings,
        steps=parse_string_list(recipe.steps)
    )

def dto_to_recipe(dto: RecipeDTO, recipe: Optional[Recipe] = None) -> Recipe:
    """
    Convert a RecipeDTO back to a SQLAlchemy Recipe.
    If `recipe` is provided, updates it; otherwise creates a new one.
    """
    if recipe is None:
        recipe = Recipe()

    recipe.name = dto.name
    recipe.description = dto.description
    recipe.ingredients_raw_str = stringify_list(dto.ingredients)
    recipe.serving_size_grams = dto.serving_size_grams
    recipe.servings = dto.servings
    recipe.steps = stringify_list(dto.steps)

    return recipe