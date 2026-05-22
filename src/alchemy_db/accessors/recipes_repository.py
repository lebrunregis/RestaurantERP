from typing import Optional

from sqlalchemy.orm import Session
from ..models.recipes_model import Recipe

# --- CRUD Accessors for Recipe --- #

# Create a new recipe
def create_recipe(
    db: Session,
    name: str,
    description: str,
    ingredients_raw_str: str,
    serving_size_grams: int,
    servings: int,
    steps: str
) -> Recipe:
    new_recipe = Recipe(
        name=name,
        description=description,
        ingredients_raw_str=ingredients_raw_str,
        serving_size_grams=serving_size_grams,
        servings=servings,
        steps=steps
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


# Get recipe by ID
def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[Recipe]:
  recipe :Optional[Recipe] =db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
  return recipe

# Get all recipes
def get_all_recipes(db: Session) -> list[Recipe]:
    return db.query(Recipe).all()

# Update a recipe
def update_recipe(
    db: Session,
    recipe_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    ingredients_raw_str: Optional[str] = None,
    serving_size_grams: Optional[int] = None,
    servings: Optional[int] = None,
    steps: Optional[str] = None
) -> Optional[Recipe]:
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        return None
    if name is not None:
        recipe.name = name
    if description is not None:
        recipe.description = description
    if ingredients_raw_str is not None:
        recipe.ingredients_raw_str = ingredients_raw_str
    if serving_size_grams is not None:
        recipe.serving_size_grams = serving_size_grams
    if servings is not None:
        recipe.servings = servings
    if steps is not None:
        recipe.steps = steps
    db.commit()
    db.refresh(recipe)
    return recipe


# Delete a recipe
def delete_recipe(db: Session, recipe_id: int) -> bool:
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        return False
    db.delete(recipe)
    db.commit()
    return True

def get_recipes_paginated(db: Session, page: int = 1, per_page: int = 50) -> list[Recipe]:
    """Return a page of recipes"""
    offset = (page - 1) * per_page
    return db.query(Recipe).offset(offset).limit(per_page).all()

def count_recipes(db: Session) -> int:
    """Return total number of recipes"""
    return db.query(Recipe).count()