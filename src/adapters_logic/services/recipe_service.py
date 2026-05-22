from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from ..dtos.recipe_dto import RecipeDTO
from ..mappers.recipe_mapper import recipe_to_dto, dto_to_recipe
from src.alchemy_db.accessors.recipes_repository import (
    count_recipes as db_count_recipes,
    create_recipe as db_create_recipe,
    get_recipe_by_id as db_get_recipe_by_id,
    get_all_recipes as db_get_all_recipes,
    update_recipe as db_update_recipe,
    delete_recipe as db_delete_recipe,
    get_recipes_paginated as db_get_recipes_paginated
)

def get_all_recipes(db: Session) -> List[RecipeDTO]:
    """Fetch all recipes from DB and convert to DTOs"""
    recipes = db_get_all_recipes(db)
    return [recipe_to_dto(r) for r in recipes]

def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[RecipeDTO]:
    recipe = db_get_recipe_by_id(db, recipe_id)
    return recipe_to_dto(recipe) if recipe else None

def create_recipe(db: Session, dto: RecipeDTO) -> RecipeDTO:
    """Create a recipe from a DTO"""
    recipe_model = dto_to_recipe(dto)
    recipe_model = db_create_recipe(
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
    """Update a recipe by ID using a DTO"""
    updated_model = db_update_recipe(
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
    return db_delete_recipe(db, recipe_id)

def get_recipes_paginated(db: Session, page: int = 1, per_page: int = 50) -> Tuple[List[RecipeDTO], int]:
    """
    Fetch a page of recipes from DB and convert to DTOs.
    Returns (list of DTOs, total count of recipes)
    """
    recipes = db_get_recipes_paginated(db, page, per_page)
    recipesDTOs = [recipe_to_dto(r) for r in recipes]
    total = db_count_recipes(db)
    return (recipesDTOs, total)