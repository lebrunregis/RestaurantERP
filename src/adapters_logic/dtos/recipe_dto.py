# adapters_logic/dtos/recipe_dto.py
from typing import List

class RecipeDTO:
    def __init__(
        self,
        recipe_id: int,
        name: str,
        description: str,
        ingredients: List[str],
        serving_size_grams: int,
        servings: int,
        steps: List[str]
    ):
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.serving_size_grams = serving_size_grams
        self.servings = servings
        self.steps = steps