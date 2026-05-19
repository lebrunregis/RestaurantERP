from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base_model import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    ingredient_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False
    )


    def __repr__(self):
        return f'Recipe : ID : {self.ingredient_id} NAME : {self.name}'