from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base_model import Base

class ClientOrder(Base):
    __tablename__ = "client_orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"))
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    served: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(String(200), nullable=True)  # special instructions

    client = relationship("Client", back_populates="orders")
    items = relationship("ClientOrderItem", back_populates="order", cascade="all, delete-orphan")