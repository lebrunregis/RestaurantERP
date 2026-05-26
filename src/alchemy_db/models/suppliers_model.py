
from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.alchemy_db.models.base_model import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    supplier_type: Mapped[str] = mapped_column(String(50), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_terms: Mapped[str] = mapped_column(String(50), nullable=False)
    lead_time_days: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


    # Link to SupplierIngredient
    ingredient_links = relationship("SupplierIngredient", back_populates="supplier_links")
    