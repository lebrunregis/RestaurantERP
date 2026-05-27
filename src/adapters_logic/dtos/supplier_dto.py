from dataclasses import dataclass
from typing import Optional


@dataclass
class SupplierDTO:
    supplier_id: Optional[int]
    name: str
    contact_name: str
    phone_number: str
    email: str
    address: str
    supplier_type: str
    tax_id: str
    payment_terms: str
    lead_time_days: int
    rating: Optional[int] = None
    active: bool = True