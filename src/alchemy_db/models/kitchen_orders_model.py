from datetime import datetime
from sqlalchemy import DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.alchemy_db.models.base_model import Base

class KitchenOrder(Base):
    __tablename__ = "kitchen_orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.supplier_id"))
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(String(200), nullable=True)

    # Relationships
    supplier = relationship("Supplier")
    items = relationship("KitchenOrderItem", back_populates="kitchen_order_link", cascade="all, delete-orphan")
