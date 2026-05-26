# adapters_logic/dtos/recipe_dto.py
from dataclasses import dataclass
from typing import  Optional

@dataclass
class RecipeDTO:
        recipe_id:Optional[int]
        name:str
        description:str
        ingredients :list[str]
        serving_size_grams:int
        servings :int
        steps:str


