from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.alchemy_db.models.recipes_model import Recipe


@dataclass
class MenuItemDTO:
    # Primary key for the menu item
    menu_item_id :int
    # Foreign key for the recipe
    recipe_id :int

    # Price divided by 100
    price :Optional[int]

    # Name of the dish
    name :str

    # Short description
    description :str
    # Category, e.g., 'Appetizer', 'Main Course', 'Dessert'
    category :str

    # Whether this item is currently visible
    is_visible :bool

    # When the item was added to the menu
    added_on :datetime