from typing import List, Optional

from sqlalchemy.orm import Session

from src.adapters_logic.dtos.supplier_dto import SupplierDTO
from src.adapters_logic.mappers.supplier_mapper import (
    supplier_to_dto,
)
from src.alchemy_db.repositories import suppliers_repository

class SupplierService:
    def __init__(self, db: Session):
        self.db = db

    def create_supplier(self, dto: SupplierDTO) -> SupplierDTO:
        supplier = suppliers_repository.create_supplier(
            db=self.db,
            name=dto.name,
            contact_name=dto.contact_name,
            phone_number=dto.phone_number,
            email=dto.email,
            address=dto.address,
            supplier_type=dto.supplier_type,
            tax_id=dto.tax_id,
            payment_terms=dto.payment_terms,
            lead_time_days=dto.lead_time_days,
            rating=dto.rating,
            active=dto.active,
        )

        return supplier_to_dto(supplier)

    def get_supplier_by_id(self, supplier_id: int) -> Optional[SupplierDTO]:
        supplier = suppliers_repository.get_supplier_by_id(
            db=self.db,
            supplier_id=supplier_id,
        )

        if not supplier:
            return None

        return supplier_to_dto(supplier)

    def get_all_suppliers(self) -> List[SupplierDTO]:
        suppliers = suppliers_repository.get_all_suppliers(self.db)

        return [supplier_to_dto(supplier) for supplier in suppliers]

    def update_supplier(
        self,
        supplier_id: int,
        dto: SupplierDTO
    ) -> Optional[SupplierDTO]:
        supplier = suppliers_repository.update_supplier(
            db=self.db,
            supplier_id=supplier_id,
            name=dto.name,
            contact_name=dto.contact_name,
            phone_number=dto.phone_number,
            email=dto.email,
            address=dto.address,
            supplier_type=dto.supplier_type,
            tax_id=dto.tax_id,
            payment_terms=dto.payment_terms,
            lead_time_days=dto.lead_time_days,
            rating=dto.rating,
            active=dto.active,
        )

        if not supplier:
            return None

        return supplier_to_dto(supplier)

    def delete_supplier(self, supplier_id: int) -> bool:
        return suppliers_repository.delete_supplier(
            db=self.db,
            supplier_id=supplier_id,
        )