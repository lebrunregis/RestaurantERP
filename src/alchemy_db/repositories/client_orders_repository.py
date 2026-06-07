from typing import Optional

from sqlalchemy.orm import Session
from datetime import datetime
from ..models.client_order_items_model import ClientOrderItem
from ..models.client_orders_model import ClientOrder

# --- CRUD Accessors for ClientOrder --- #

# Create a new client order
def create_client_order(
    db: Session,
    client_id: int,
    order_date: Optional[datetime] = None,
    served: Optional[bool] = False,
    notes: Optional[str] = None
) -> ClientOrder:
    new_order = ClientOrder(
        client_id=client_id,
        order_date=order_date or datetime.now(),
        served=served,
        notes=notes
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


# Get client order by ID
def get_client_order_by_id(db: Session, order_id: int) -> Optional[ClientOrder]:
    return db.query(ClientOrder).filter(ClientOrder.order_id == order_id).first()


# Get all orders for a client
def get_orders_for_client(db: Session, client_id: int) -> list[ClientOrder]:
    return db.query(ClientOrder).filter(ClientOrder.client_id == client_id).all()


# Get all client orders
def get_all_client_orders(db: Session) -> list[ClientOrder]:
    return db.query(ClientOrder).all()

def get_all_client_orders_paginated(db: Session, page: int = 1, per_page: int = 50) -> list[Recipe]:
    offset = (page - 1) * per_page
    return db.query(ClientOrder).offset(offset).limit(per_page).all()


# Update a client order
def update_client_order(
    db: Session,
    order_id: int,
    served: Optional[bool] = None,
    notes: Optional[str] = None,
    order_date: Optional[datetime] = None
) -> Optional[ClientOrder]:
    order = db.query(ClientOrder).filter(ClientOrder.order_id == order_id).first()
    if not order:
        return None
    if served is not None:
        order.served = served
    if notes is not None:
        order.notes = notes
    if order_date is not None:
        order.order_date = order_date
    db.commit()
    db.refresh(order)
    return order


# Delete a client order (cascade deletes items)
def delete_client_order(db: Session, order_id: int) -> bool:
    order = db.query(ClientOrder).filter(ClientOrder.order_id == order_id).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True


# --- Relationship Accessors for ClientOrder --- #

# Get all items for a given order
def get_items_for_order(db: Session, order_id: int) -> list[ClientOrderItem]:
    order = db.query(ClientOrder).filter(ClientOrder.order_id == order_id).first()
    if order:
        return order.items  # returns list of ClientOrderItem
    return []


# Add an item to a client order
def add_item_to_order(db: Session, order_id: int, 
    menu_item_id :int,
    quantity: int,
    price :float ,
    notes:str) -> Optional[ClientOrderItem]:
    new_order_item = ClientOrderItem(
        order_id=order_id,
        menu_item_id= menu_item_id,
        quantity=quantity,
        price=price,
        notes=notes
    )
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    return new_order_item

def update_client_order_item(
    db: Session,
    order_id:int,
    menu_item_id:int,
    quantity:int,
    price:float,
    notes:str
) -> Optional[ClientOrderItem]:
    orderItem = db.query(ClientOrderItem).filter(ClientOrderItem.order_id == order_id, ClientOrderItem.menu_item_id == menu_item_id).first()
    if not orderItem:
        return None
    if quantity is not None:
        orderItem.quantity = quantity
    if notes is not None:
        orderItem.notes = notes
    if price is not None:
        orderItem.price = price
    db.commit()
    db.refresh(orderItem)
    return orderItem



# Remove an item from a client order
def remove_item_from_order(db: Session, order_id: int, item_id: int) -> bool:
    order = db.query(ClientOrder).filter(ClientOrder.order_id == order_id).first()
    if not order:
        return False
    item_to_remove = next((i for i in order.items if i.id == item_id), None)
    if item_to_remove:
        order.items.remove(item_to_remove)
        db.delete(item_to_remove)
        db.commit()
        return True
    return False