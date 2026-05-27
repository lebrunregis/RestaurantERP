from typing import Optional

from src.adapters_logic.dtos.supplier_dto import SupplierDTO
from src.alchemy_db.models.suppliers_model import Supplier


def supplier_to_dto(supplier: Supplier) -> SupplierDTO:
    return SupplierDTO(
        supplier_id=supplier.supplier_id,
        name=supplier.name,
        contact_name=supplier.contact_name,
        phone_number=supplier.phone_number,
        email=supplier.email,
        address=supplier.address,
        supplier_type=supplier.supplier_type,
        tax_id=supplier.tax_id,
        payment_terms=supplier.payment_terms,
        lead_time_days=supplier.lead_time_days,
        rating=supplier.rating,
        active=supplier.active,
    )


def dto_to_supplier(
    dto: SupplierDTO,
    supplier: Optional[Supplier] = None
) -> Supplier:
    """
    Convert SupplierDTO to Supplier model.
    
    If a Supplier instance is provided, it updates the existing instance.
    Otherwise, it creates a new Supplier instance.
    """

    if supplier is None:
        supplier = Supplier()

    supplier.name = dto.name
    supplier.contact_name = dto.contact_name
    supplier.phone_number = dto.phone_number
    supplier.email = dto.email
    supplier.address = dto.address
    supplier.supplier_type = dto.supplier_type
    supplier.tax_id = dto.tax_id
    supplier.payment_terms = dto.payment_terms
    supplier.lead_time_days = dto.lead_time_days
    supplier.rating = dto.rating
    supplier.active = dto.active

    return supplier