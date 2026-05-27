from datetime import datetime
from dataclasses import dataclass

@dataclass
class ClientOrderItemDTO:
    order_id :int
    menu_item_id :int
    quantity: int
    price :float 
    notes:str

@dataclass
class ClientOrderDTO:
    order_id: int
    client_id: int
    order_date: datetime
    served: bool
    notes: str

