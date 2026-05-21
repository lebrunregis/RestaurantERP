from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, String, ForeignKey
from datetime import datetime

from src.alchemy_db.models.recipes_model import Recipe

from .base_model import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    # Primary key for the menu item
    menu_item_id: Mapped[int] = mapped_column(primary_key=True)
    
    # Foreign key for the recipe
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.recipe_id"))

    # Price divided by 100
    price: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)

    # Name of the dish
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Short description
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Category, e.g., 'Appetizer', 'Main Course', 'Dessert'
    category: Mapped[str] = mapped_column(String(50), nullable=True)

    # Whether this item is currently visible
    is_visible: Mapped[bool] = mapped_column(default=True)

    # When the item was added to the menu
    added_on: Mapped[datetime] = mapped_column(default=datetime.now)

    recipe_link: Mapped[Recipe] = relationship("Recipe")

    # Add index to speed up queries grouped by ingredient_id
    __table_args__ = (
        Index("ix_menu_item_recipe_id", "recipe_id"),

    )
    def __repr__(self):
        status = "Visible" if self.is_visible else "Invisible"
        return f"<MenuItem {self.name} (${self.price}) - {status}>"