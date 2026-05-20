from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base_model import Base

class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # full name
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(200), nullable=True)  # for delivery
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Link to orders
    orders = relationship("ClientOrder", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client(id={self.client_id}, name={self.name}, email={self.email})>"