from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from ..dtos.recipe_dto import RecipeDTO
from ..mappers.recipe_mapper import recipe_to_dto, dto_to_recipe
from src.alchemy_db.repositories import recipes_repository

def get_all_recipes(db: Session) -> List[RecipeDTO]:
    recipes = recipes_repository.get_all_recipes(db)
    return [recipe_to_dto(r) for r in recipes]

def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[RecipeDTO]:
    recipe = recipes_repository.get_recipe_by_id(db, recipe_id)
    return recipe_to_dto(recipe) if recipe else None

def create_recipe(db: Session, dto: RecipeDTO) -> RecipeDTO:
    recipe_model = dto_to_recipe(dto)
    recipe_model = recipes_repository.create_recipe(
        db,
        name=recipe_model.name,
        description=recipe_model.description,
        ingredients_raw_str=recipe_model.ingredients_raw_str,
        serving_size_grams=recipe_model.serving_size_grams,
        servings=recipe_model.servings,
        steps=recipe_model.steps
    )
    return recipe_to_dto(recipe_model)

def update_recipe(db: Session, recipe_id: int, dto: RecipeDTO) -> Optional[RecipeDTO]:
    updated_model = recipes_repository.update_recipe(
        db,
        recipe_id=recipe_id,
        name=dto.name,
        description=dto.description,
        ingredients_raw_str=str(dto.ingredients),
        serving_size_grams=dto.serving_size_grams,
        servings=dto.servings,
        steps=str(dto.steps)
    )
    return recipe_to_dto(updated_model) if updated_model else None

def delete_recipe(db: Session, recipe_id: int) -> bool:
    return delete_recipe(db, recipe_id)

def get_recipes_paginated(db: Session, page: int = 1, per_page: int = 50) -> Tuple[List[RecipeDTO], int]:
    recipes = recipes_repository.get_recipes_paginated(db, page, per_page)
    recipesDTOs = [recipe_to_dto(r) for r in recipes]
    total = recipes_repository.count_recipes(db)
    return (recipesDTOs, total)

def get_top_matching_recipes_by_ingredients(db: Session, ingredients: list[str])-> list[RecipeDTO]:
    recipes =  get_top_matching_recipes_by_ingredients(db,ingredients)
    return [recipe_to_dto(r) for r in recipes]

def get_recipes_containing_in_name (db: Session, substr: str)-> list[RecipeDTO]:
  recipes =   recipes_repository.get_recipes_containing_in_name(db, substr)
  return [recipe_to_dto(r) for r in recipes]
  
def get_recipes_containing_in_name_paginated (db: Session, substr: str, page: int = 1, per_page: int = 50)-> list[RecipeDTO]:
    recipes =   recipes_repository.get_recipes_containing_in_name_paginated(db, substr,  page, per_page)
    return [recipe_to_dto(r) for r in recipes]
  
def get_top_matching_recipes_by_ingredients_paginated(db: Session, ingredients: list[str], page: int = 1, per_page: int = 50) -> tuple[list[tuple[RecipeDTO,int]], int]:
    result =  recipes_repository.get_top_matching_recipes_by_ingredients_paginated(db,ingredients, page, per_page)
    results = result[0]
    amount = result[1]
    recipesDTO = [(recipe_to_dto(result[0]),result[1]) for result in results]
    print(f"converted {len(recipesDTO)} DTOS")
    return (recipesDTO, amount)