from typing import Optional

from src.adapters_logic.dtos.kitchen_order_dto import (
    KitchenOrderDTO,
    KitchenOrderItemDTO,
)
from src.alchemy_db.models.kitchen_order_items_model import KitchenOrderItem
from src.alchemy_db.models.kitchen_orders_model import (
    KitchenOrder,
)


def kitchen_order_item_to_dto(
    order_item: KitchenOrderItem
) -> KitchenOrderItemDTO:
    return KitchenOrderItemDTO(
        order_id=order_item.order_id,
        ingredient_id=order_item.ingredient_id,
        quantity=order_item.quantity,
        unit=order_item.unit,
        price_per_unit=order_item.price_per_unit,
        ingredient_name=order_item.ingredient_link.ingredient_name,
    )


def dto_to_kitchen_order_item(
    dto: KitchenOrderItemDTO,
    order_item: Optional[KitchenOrderItem] = None
) -> KitchenOrderItem:

    if order_item is None:
        order_item = KitchenOrderItem()

    order_item.order_id = dto.order_id
    order_item.ingredient_id = dto.ingredient_id
    order_item.quantity = dto.quantity
    order_item.unit = dto.unit
    order_item.price_per_unit = dto.price_per_unit

    return order_item


def kitchen_order_to_dto(
    order: KitchenOrder
) -> KitchenOrderDTO:
    return KitchenOrderDTO(
        order_id=order.order_id,
        supplier_id=order.supplier_id,
        order_date=order.order_date,
        delivered=order.delivered,
        notes=order.notes,
        supplier_name=order.supplier.supplier_name,
    )


def dto_to_kitchen_order(
    dto: KitchenOrderDTO,
    order: Optional[KitchenOrder] = None
) -> KitchenOrder:

    if order is None:
        order = KitchenOrder()

    order.order_id = dto.order_id
    order.supplier_id = dto.supplier_id
    order.order_date = dto.order_date
    order.delivered = dto.delivered
    order.notes = dto.notes

    return order