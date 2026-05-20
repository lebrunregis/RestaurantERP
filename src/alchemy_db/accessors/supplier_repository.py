from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.suppliers_model import Supplier
from ..models.supplier_ingredient_model import SupplierIngredient


# --- CRUD Accessors for Supplier --- #

def create_supplier(
    db: Session,
    name: str,
    contact_name: Optional[str] = None,
    phone_number: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    supplier_type: Optional[str] = None,
    tax_id: Optional[str] = None,
    payment_terms: Optional[str] = None,
    lead_time_days: Optional[int] = None,
    rating: Optional[int] = None,
    active: bool = True
) -> Supplier:
    new_supplier = Supplier(
        name=name,
        contact_name=contact_name,
        phone_number=phone_number,
        email=email,
        address=address,
        supplier_type=supplier_type,
        tax_id=tax_id,
        payment_terms=payment_terms,
        lead_time_days=lead_time_days,
        rating=rating,
        active=active
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier


def get_supplier_by_id(db: Session, supplier_id: int) -> Optional[Supplier]:
    return db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()


def get_all_suppliers(db: Session) -> List[Supplier]:
    return db.query(Supplier).all()


def update_supplier(
    db: Session,
    supplier_id: int,
    name: Optional[str] = None,
    contact_name: Optional[str] = None,
    phone_number: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    supplier_type: Optional[str] = None,
    tax_id: Optional[str] = None,
    payment_terms: Optional[str] = None,
    lead_time_days: Optional[int] = None,
    rating: Optional[int] = None,
    active: Optional[bool] = None
) -> Optional[Supplier]:
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return None
    if name is not None:
        supplier.name = name
    if contact_name is not None:
        supplier.contact_name = contact_name
    if phone_number is not None:
        supplier.phone_number = phone_number
    if email is not None:
        supplier.email = email
    if address is not None:
        supplier.address = address
    if supplier_type is not None:
        supplier.supplier_type = supplier_type
    if tax_id is not None:
        supplier.tax_id = tax_id
    if payment_terms is not None:
        supplier.payment_terms = payment_terms
    if lead_time_days is not None:
        supplier.lead_time_days = lead_time_days
    if rating is not None:
        supplier.rating = rating
    if active is not None:
        supplier.active = active
    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(db: Session, supplier_id: int) -> bool:
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return False
    db.delete(supplier)
    db.commit()
    return True


# --- Relationship Accessors for SupplierIngredient --- #

def get_ingredients_for_supplier(db: Session, supplier_id: int) -> List[SupplierIngredient]:
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if supplier:
        return supplier.ingredient_links
    return []


def add_ingredient_to_supplier(db: Session, supplier_id: int, ingredient_link: SupplierIngredient) -> bool:
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return False
    supplier.ingredient_links.append(ingredient_link)
    db.commit()
    return True


def remove_ingredient_from_supplier(db: Session, supplier_id: int, ingredient_link_id: int) -> bool:
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        return False
    link_to_remove = next((link for link in supplier.ingredient_links if link.id == ingredient_link_id), None)
    if link_to_remove:
        supplier.ingredient_links.remove(link_to_remove)
        db.delete(link_to_remove)
        db.commit()
        return True
    return False