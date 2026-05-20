from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base_model import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    ingredient_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    # Link to SupplierIngredient
    supplier_links = relationship("SupplierIngredient", back_populates="ingredient_links")
        # Link to RecipeIngredient
    recipe_links = relationship("RecipeIngredient", back_populates="ingredient_links", cascade="all, delete-orphan")