from datetime import datetime
from dataclasses import dataclass

@dataclass
class KitchenOrderItemDTO:
    order_id:  int
    ingredient_id:  int
    quantity:  float
    unit:  str
    price_per_unit:  float
    ingredient_name:  str


@dataclass
class KitchenOrderDTO:
    order_id:  int
    supplier_id:  int
    order_date:  datetime
    delivered:  bool
    notes:  str
    supplier_name :str