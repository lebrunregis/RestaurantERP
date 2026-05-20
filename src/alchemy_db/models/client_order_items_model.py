from sqlalchemy import ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class ClientOrderItem(Base):
    __tablename__ = "client_order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("client_orders.order_id"), primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.menu_item_id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)  # store price at time of order
    notes: Mapped[str] = mapped_column(String(200), nullable=True)  # e.g., "extra cheese"

    # Relationships
    order = relationship("ClientOrder", back_populates="items")
    menu_item = relationship("MenuItem")