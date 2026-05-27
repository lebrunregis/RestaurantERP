from typing import Optional

from src.adapters_logic.dtos.menu_item_dto import MenuItemDTO
from src.alchemy_db.models.menu_items_model import MenuItem


def menu_item_to_dto(menu_item: MenuItem) -> MenuItemDTO:
    return MenuItemDTO(
        menu_item_id=menu_item.menu_item_id,
        recipe_id=menu_item.recipe_id,
        price=menu_item.price,
        name=menu_item.name,
        description=menu_item.description,
        category=menu_item.category,
        is_visible=menu_item.is_visible,
        added_on=menu_item.added_on,
    )


def dto_to_menu_item(
    dto: MenuItemDTO,
    menu_item: Optional[MenuItem] = None
) -> MenuItem:

    if menu_item is None:
        menu_item = MenuItem()

    menu_item.menu_item_id = dto.menu_item_id
    menu_item.recipe_id = dto.recipe_id
    menu_item.price = dto.price
    menu_item.name = dto.name
    menu_item.description = dto.description
    menu_item.category = dto.category
    menu_item.is_visible = dto.is_visible
    menu_item.added_on = dto.added_on

    return menu_item