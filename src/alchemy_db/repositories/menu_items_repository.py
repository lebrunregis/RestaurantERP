from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.menu_items_model import MenuItem
from ..models.menu_items_model import Recipe


# --- CRUD Accessors for MenuItem --- #

def create_menu_item(
    db: Session,
    recipe_id: int,
    name: str,
    price: Optional[int] = 0,
    description: Optional[str] = None,
    category: Optional[str] = None,
    is_visible: bool = True,
    added_on: Optional[datetime] = None
) -> MenuItem:
    new_item = MenuItem(
        recipe_id=recipe_id,
        name=name,
        price=price,
        description=description,
        category=category,
        is_visible=is_visible,
        added_on=added_on or datetime.now()
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_menu_item_by_id(db: Session, menu_item_id: int) -> Optional[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.menu_item_id == menu_item_id).first()


def get_all_menu_items(db: Session) -> List[MenuItem]:
    return db.query(MenuItem).all()


def get_visible_menu_items(db: Session) -> List[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.is_visible == True).all()


def update_menu_item(
    db: Session,
    menu_item_id: int,
    recipe_id: Optional[int] = None,
    name: Optional[str] = None,
    price: Optional[int] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    is_visible: Optional[bool] = None
) -> Optional[MenuItem]:
    item = db.query(MenuItem).filter(MenuItem.menu_item_id == menu_item_id).first()
    if not item:
        return None
    if recipe_id is not None:
        item.recipe_id = recipe_id
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if description is not None:
        item.description = description
    if category is not None:
        item.category = category
    if is_visible is not None:
        item.is_visible = is_visible
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, menu_item_id: int) -> bool:
    item = db.query(MenuItem).filter(MenuItem.menu_item_id == menu_item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def get_menu_items_paginated(db: Session, page: int = 1, per_page: int = 50) -> list[Recipe]:
    offset = (page - 1) * per_page
    return db.query(Recipe).offset(offset).limit(per_page).all()

def count_menu_items(db: Session) -> int:
    return db.query(Recipe).count()

def get_menu_items_containing_in_name(db: Session, substr: str) -> list[Recipe]:
   return db.query(Recipe).filter(Recipe.name.ilike(f"%{substr}%")).all()

def get_menu_items_containing_in_name_paginated(db: Session, substr: str,  page: int = 1, per_page: int = 50) -> list[Recipe]:
   offset = (page - 1) * per_page
   return db.query(Recipe).filter(Recipe.name.ilike(f"%{substr}%")).offset(offset).limit(per_page).all()


# --- Relationship Accessor for Recipe --- #

def get_recipe_for_menu_item(db: Session, menu_item_id: int) -> Optional[Recipe]:
    item = db.query(MenuItem).filter(MenuItem.menu_item_id == menu_item_id).first()
    if item:
        return item.recipe_link
    return None