from sqlalchemy import ForeignKey, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class KitchenOrderItem(Base):
    __tablename__ = "kitchen_order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("kitchen_orders.order_id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.ingredient_id"), primary_key=True)  
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=True)

    # Relationships
    kitchen_order_link = relationship("KitchenOrder", back_populates="items")
    ingredient_link = relationship("Ingredient")