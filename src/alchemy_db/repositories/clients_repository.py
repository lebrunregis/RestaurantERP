from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from ..models.clients_model import Client
from ..models.client_orders_model import  ClientOrder


# --- CRUD Accessors for Client --- #

def create_client(
    db: Session,
    name: str,
    email: str,
    phone_number: Optional[str] = None,
    address: Optional[str] = None,
    created_at: Optional[datetime] = None
) -> Client:
    new_client = Client(
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
        created_at=created_at or datetime.now()
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


def get_client_by_id(db: Session, client_id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.client_id == client_id).first()


def get_client_by_email(db: Session, email: str) -> Optional[Client]:
    return db.query(Client).filter(Client.email == email).first()


def get_all_clients(db: Session) -> List[Client]:
    return db.query(Client).all()

def get_clients_paginated(db: Session, page: int = 1, per_page: int = 50) -> List[Client]:
    offset = (page - 1) * per_page
    return db.query(Client).offset(offset).limit(per_page).all()


def count_clients(db: Session) -> int:
    return db.query(Client).count()

def get_clients_containing_in_name(db: Session, substr: str) -> list[Client]:
   return db.query(Client).filter(or_(Client.full_name.ilike(f"%{substr}%",))).all()

def get_clients_containing_in_name_paginated(db: Session, substr: str,  page: int = 1, per_page: int = 50) -> list[Client]:
   offset = (page - 1) * per_page
   return db.query(Client).filter(or_(Client.full_name.ilike(f"%{substr}%"))).offset(offset).limit(per_page).all()


def update_client(
    db: Session,
    client_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    address: Optional[str] = None
) -> Optional[Client]:
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        return None
    if name is not None:
        client.full_name = name
    if email is not None:
        client.email = email
    if phone_number is not None:
        client.phone_number = phone_number
    if address is not None:
        client.address = address
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int) -> bool:
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True


# --- Relationship Accessors for Client --- #

def get_orders_for_client(db: Session, client_id: int) -> List[ClientOrder]:
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if client:
        return client.orders
    return []


def add_order_to_client(db: Session, client_id: int, order: ClientOrder) -> bool:
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        return False
    client.orders.append(order)
    db.commit()
    return True


def remove_order_from_client(db: Session, client_id: int, order_id: int) -> bool:
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        return False
    order_to_remove = next((o for o in client.orders if o.order_id == order_id), None)
    if order_to_remove:
        client.orders.remove(order_to_remove)
        db.delete(order_to_remove)
        db.commit()
        return True
    return False