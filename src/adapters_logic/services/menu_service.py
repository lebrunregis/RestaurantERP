from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from ..dtos.menu_item_dto import MenuItemDTO
from ..mappers.menu_item_mapper import menu_item_to_dto, dto_to_menu_item
from src.alchemy_db.repositories import menu_items_repository

def get_all_menu_items(db: Session) -> List[MenuItemDTO]:
    menu_items = menu_items_repository.get_all_menu_items(db)
    return [menu_item_to_dto(r) for r in menu_items]

def get_menu_item_by_id(db: Session, menu_item_id: int) -> Optional[MenuItemDTO]:
    menu_item = menu_items_repository.get_menu_item_by_id(db, menu_item_id)
    return menu_item_to_dto(menu_item) if menu_item else None

def create_menu_item(db: Session, dto: MenuItemDTO) -> MenuItemDTO:
    menu_item_model = dto_to_menu_item(dto)
    menu_item_model = menu_items_repository.create_menu_item(
        db,

    )
    return menu_item_to_dto(menu_item_model)

def update_menu_item(db: Session, menu_item_id: int, dto: MenuItemDTO) -> Optional[MenuItemDTO]:
    updated_model = menu_items_repository.update_menu_item(
        db,
        menu_item_id=menu_item_id,
        name=dto.name,
        description=dto.description,

    )
    return menu_item_to_dto(updated_model) if updated_model else None

def delete_menu_item(db: Session, menu_item_id: int) -> bool:
    return delete_menu_item(db, menu_item_id)

def get_menu_items_paginated(db: Session, page: int = 1, per_page: int = 50) -> Tuple[List[MenuItemDTO], int]:
    menu_items = menu_items_repository.get_menu_items_paginated(db, page, per_page)
    menu_itemsDTOs = [menu_item_to_dto(r) for r in menu_items]
    total = menu_items_repository.count_menu_items(db)
    return (menu_itemsDTOs, total)

def get_menu_items_containing_in_name (db: Session, substr: str)-> list[MenuItemDTO]:
  menu_items =   menu_items_repository.get_menu_items_containing_in_name(db, substr)
  return [menu_item_to_dto(r) for r in menu_items]
  
def get_menu_items_containing_in_name_paginated (db: Session, substr: str, page: int = 1, per_page: int = 50)-> list[MenuItemDTO]:
    menu_items =   menu_items_repository.get_menu_items_containing_in_name_paginated(db, substr,  page, per_page)
    return [menu_item_to_dto(r) for r in menu_items]