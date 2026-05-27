from typing import Optional

from sqlalchemy.orm import Session

from ..models.recipe_ingredients_model import RecipeIngredient
from ..models.supplier_ingredient_model import SupplierIngredient
from ..models.ingredients_model import Ingredient

# Create a new ingredient
def create_ingredient(db: Session, name: str) -> Ingredient:
    new_ingredient = Ingredient(name=name)
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient


# Get ingredient by ID
def get_ingredient_by_id(db: Session, ingredient_id: int) -> Optional[Ingredient]:
    return db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()


# Get ingredient by name
def get_ingredient_by_name(db: Session, name: str) -> Optional[Ingredient]:
    return db.query(Ingredient).filter(Ingredient.name == name).first()


# Get all ingredients
def get_all_ingredients(db: Session) -> list[Ingredient]:
    return db.query(Ingredient).all()


# Update an ingredient
def update_ingredient(db: Session, ingredient_id: int, new_name: str) -> Optional[Ingredient]:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        return None
    ingredient.name = new_name
    db.commit()
    db.refresh(ingredient)
    return ingredient


# Delete an ingredient
def delete_ingredient(db: Session, ingredient_id: int) -> bool:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        return False
    db.delete(ingredient)
    db.commit()
    return True

# --- Ingredient Relationships Accessors --- #

# Get all recipes for a given ingredient
def get_recipes_for_ingredient(db: Session, ingredient_id: int) -> list[RecipeIngredient]:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if ingredient:
        return ingredient.recipe_ingredient_links  # returns list of RecipeIngredient
    return []


# Get all suppliers for a given ingredient
def get_suppliers_for_ingredient(db: Session, ingredient_id: int) -> list[SupplierIngredient]:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if ingredient:
        return ingredient.supplier_links  # returns list of SupplierIngredient
    return []


# Add a recipe link to an ingredient
def add_recipe_to_ingredient(db: Session, ingredient_id: int, recipe_ingredient: RecipeIngredient) -> bool:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        return False
    ingredient.recipe_ingredient_links.append(recipe_ingredient)
    db.commit()
    return True


# Remove a recipe link from an ingredient
def remove_recipe_from_ingredient(db: Session, ingredient_id: int, recipe_ingredient_id: int) -> bool:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        return False
    link_to_remove = next((link for link in ingredient.recipe_ingredient_links if link.id == recipe_ingredient_id), None)
    if link_to_remove:
        ingredient.recipe_ingredient_links.remove(link_to_remove)
        db.delete(link_to_remove)
        db.commit()
        return True
    return False


# Add a supplier link to an ingredient
def add_supplier_to_ingredient(db: Session, ingredient_id: int, supplier_ingredient: SupplierIngredient) -> bool:
    ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        return False
    ingredient.supplier_links.append(supplier_ingredient)
    db.commit()
    return True
