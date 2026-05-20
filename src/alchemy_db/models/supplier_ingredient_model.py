from sqlalchemy import String, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class SupplierIngredient(Base):
    __tablename__ = "supplier_ingredients"

    # Composite primary key
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.supplier_id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.ingredient_id"), primary_key=True)

    # Additional fields
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=True)  # optional cost
    remaining_units: Mapped[int] = mapped_column(Integer, default=0)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., kg, liters, pieces

    # Relationships
    supplier_links = relationship("Supplier", back_populates="ingredient_links")
    ingredient_links = relationship("Ingredient", back_populates="supplier_links")