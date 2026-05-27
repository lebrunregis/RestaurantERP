from typing import List, Optional

from sqlalchemy.orm import Session

from src.adapters_logic.dtos.supplier_dto import SupplierDTO
from src.adapters_logic.mappers.supplier_mapper import (
    supplier_to_dto,
)
from src.alchemy_db.repositories import suppliers_repository

def create_supplier(db: Session, dto: SupplierDTO) -> SupplierDTO:
        supplier = suppliers_repository.create_supplier(
            db=db,
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

def get_supplier_by_id(db: Session, supplier_id: int) -> Optional[SupplierDTO]:
        supplier = suppliers_repository.get_supplier_by_id(
            db=db,
            supplier_id=supplier_id,
        )

        if not supplier:
            return None

        return supplier_to_dto(supplier)

def get_all_suppliers(db: Session) -> List[SupplierDTO]:
        suppliers = suppliers_repository.get_all_suppliers(db)

        return [supplier_to_dto(supplier) for supplier in suppliers]

def get_suppliers_paginated(
        db: Session,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[list[SupplierDTO],int]:
        suppliers = suppliers_repository.get_suppliers_paginated(
            db=db,
            page=page,
            page_size=page_size,
        )

        return ([supplier_to_dto(supplier) for supplier in suppliers[0]],suppliers[1])

def get_suppliers_containing_in_name_paginated(
        db: Session,
        name: str,
        page: int = 1,
        page_size: int = 20
    ) -> List[SupplierDTO]:
        suppliers = suppliers_repository.get_suppliers_containing_in_name_paginated(
            db=db,
            name=name,
            page=page,
            page_size=page_size,
        )

        return [supplier_to_dto(supplier) for supplier in suppliers]

def update_supplier(
        db: Session,
        supplier_id: int,
        dto: SupplierDTO
    ) -> Optional[SupplierDTO]:
        supplier = suppliers_repository.update_supplier(
            db=db,
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

def delete_supplier(db: Session, supplier_id: int) -> bool:
        return suppliers_repository.delete_supplier(
            db=db,
            supplier_id=supplier_id,
        )