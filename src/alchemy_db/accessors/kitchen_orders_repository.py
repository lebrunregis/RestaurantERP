from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.kitchen_orders_model import KitchenOrder
from ..models.kitchen_order_items_model import KitchenOrderItem
from ..models.suppliers_model import Supplier


# --- CRUD Accessors for KitchenOrder --- #

def create_kitchen_order(
    db: Session,
    supplier_id: int,
    order_date: Optional[datetime] = None,
    delivered: bool = False,
    notes: Optional[str] = None
) -> KitchenOrder:
    new_order = KitchenOrder(
        supplier_id=supplier_id,
        order_date=order_date or datetime.now(),
        delivered=delivered,
        notes=notes
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_kitchen_order_by_id(db: Session, order_id: int) -> Optional[KitchenOrder]:
    return db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()


def get_all_kitchen_orders(db: Session) -> List[KitchenOrder]:
    return db.query(KitchenOrder).all()


def get_orders_for_supplier(db: Session, supplier_id: int) -> List[KitchenOrder]:
    return db.query(KitchenOrder).filter(KitchenOrder.supplier_id == supplier_id).all()


def update_kitchen_order(
    db: Session,
    order_id: int,
    supplier_id: Optional[int] = None,
    order_date: Optional[datetime] = None,
    delivered: Optional[bool] = None,
    notes: Optional[str] = None
) -> Optional[KitchenOrder]:
    order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not order:
        return None
    if supplier_id is not None:
        order.supplier_id = supplier_id
    if order_date is not None:
        order.order_date = order_date
    if delivered is not None:
        order.delivered = delivered
    if notes is not None:
        order.notes = notes
    db.commit()
    db.refresh(order)
    return order


def delete_kitchen_order(db: Session, order_id: int) -> bool:
    order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True


# --- Relationship Accessors --- #

def get_supplier_for_order(db: Session, order_id: int) -> Optional[Supplier]:
    order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if order:
        return order.supplier
    return None


def get_items_for_order(db: Session, order_id: int) -> List[KitchenOrderItem]:
    order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if order:
        return order.items
    return []


def add_item_to_order(db: Session, order_id: int, item: KitchenOrderItem) -> bool:
    order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not order:
        return False
    order.items.append(item)
    db.commit()
    return True


def remove_item_from_order(db: Session, order_id: int, item_id: int) -> bool:
    order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not order:
        return False
    item_to_remove = next((i for i in order.items if i.id == item_id), None)
    if item_to_remove:
        order.items.remove(item_to_remove)
        db.delete(item_to_remove)
        db.commit()
        return True
    return False