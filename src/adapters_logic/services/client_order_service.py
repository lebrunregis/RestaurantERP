from typing import List, Optional

from sqlalchemy.orm import Session

from src.adapters_logic.dtos.client_order_dto import ClientOrderDTO, ClientOrderItemDTO
from src.adapters_logic.mappers.client_order_mapper import (
    client_order_to_dto,
    client_order_item_to_dto,
)
from src.alchemy_db.repositories import client_orders_repository

def create_order(db: Session, dto: ClientOrderDTO) -> ClientOrderDTO:
        order = client_orders_repository.create_client_order(
            db=db,
            client_id=dto.client_id,
            order_date=dto.order_date,
            served=dto.served,
            notes=dto.notes,  # assume repository handles item creation
        )

        return client_order_to_dto(order)

def get_client_order_by_id(db: Session, order_id: int) -> Optional[ClientOrderDTO]:
        order = client_orders_repository.get_client_order_by_id(
            db=db,
            order_id=order_id,
        )
        if not order:
            return None
        return client_order_to_dto(order)

def get_orders_by_client(db: Session, client_id: int) -> List[ClientOrderDTO]:
        orders = client_orders_repository.get_orders_for_client(
            db=db,
            client_id=client_id,
        )
        return [client_order_to_dto(order) for order in orders]

def get_all_orders(db: Session) -> List[ClientOrderDTO]:
        orders = client_orders_repository.get_all_client_orders(db)
        return [client_order_to_dto(order) for order in orders]

def get_all_client_orders_paginated(db: Session, page: int = 1, per_page: int = 50) -> list[Recipe]:
        orders = client_orders_repository.get_all_client_orders_paginated(db,page,per_page)
        return [client_order_to_dto(order) for order in orders]


def update_order(
        db: Session,
        order_id: int,
        dto: ClientOrderDTO
    ) -> Optional[ClientOrderDTO]:
        order = client_orders_repository.update_client_order(
            db=db,
            order_id=order_id,
            order_date=dto.order_date,
            served=dto.served,
            notes=dto.notes,
        )
        if not order:
            return None
        return client_order_to_dto(order)

def delete_order(db: Session, order_id: int) -> bool:
        return client_orders_repository.delete_client_order(
            db=db,
            order_id=order_id,
        )

    # -------------------- Order Items --------------------

def add_order_item(db: Session, order_id: int, item_dto: ClientOrderItemDTO) -> Optional[ClientOrderItemDTO]:
        item = client_orders_repository.add_item_to_order(
            db=db,
            order_id=order_id,
            menu_item_id=item_dto.menu_item_id,
            quantity=item_dto.quantity,
            price=item_dto.price,
            notes=item_dto.notes
        )
        if not item:
            return None
        return client_order_item_to_dto(item)

def update_order_item(db: Session, order_id: int, item_dto: ClientOrderItemDTO) -> Optional[ClientOrderItemDTO]:
        item = client_orders_repository.update_client_order_item(
            db=db,
            order_id=order_id,
            menu_item_id=item_dto.menu_item_id,
            quantity=item_dto.quantity,
            price=item_dto.price,
            notes=item_dto.notes,
        )
        if not item:
            return None
        return client_order_item_to_dto(item)

def delete_order_item(db: Session, order_id: int, menu_item_id: int) -> bool:
        return client_orders_repository.delete_client_order(
            db=db,
            order_id=order_id
        )