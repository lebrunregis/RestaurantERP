from typing import Optional

from src.adapters_logic.dtos.client_order_dto import (
    ClientOrderDTO,
    ClientOrderItemDTO,
)
from src.alchemy_db.models.client_order_items_model import ClientOrderItem
from src.alchemy_db.models.client_orders_model import (
    ClientOrder
)


def client_order_item_to_dto(
    order_item: ClientOrderItem
) -> ClientOrderItemDTO:
    return ClientOrderItemDTO(
        order_id=order_item.order_id,
        menu_item_id=order_item.menu_item_id,
        quantity=order_item.quantity,
        price=order_item.price,
        notes=order_item.notes,
    )


def dto_to_client_order_item(
    dto: ClientOrderItemDTO,
    order_item: Optional[ClientOrderItem] = None
) -> ClientOrderItem:

    if order_item is None:
        order_item = ClientOrderItem()

    order_item.order_id = dto.order_id
    order_item.menu_item_id = dto.menu_item_id
    order_item.quantity = dto.quantity
    order_item.price = dto.price
    order_item.notes = dto.notes

    return order_item


def client_order_to_dto(
    order: ClientOrder
) -> ClientOrderDTO:
    return ClientOrderDTO(
        order_id=order.order_id,
        client_id=order.client_id,
        order_date=order.order_date,
        served=order.served,
        notes=order.notes,
    )


def dto_to_client_order(
    dto: ClientOrderDTO,
    order: Optional[ClientOrder] = None
) -> ClientOrder:

    if order is None:
        order = ClientOrder()

    order.order_id = dto.order_id
    order.client_id = dto.client_id
    order.order_date = dto.order_date
    order.served = dto.served
    order.notes = dto.notes

    return order