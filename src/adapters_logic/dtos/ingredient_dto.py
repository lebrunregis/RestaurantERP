from dataclasses import dataclass
from typing import Optional

@dataclass
class IngredientDTO:
        ingredient_id:Optional[int]
        name:str