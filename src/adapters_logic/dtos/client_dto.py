from dataclasses import dataclass
from datetime import datetime

@dataclass
class ClientDTO:
    client_id:  int
    name:  str
    email:  str
    phone_number:  str
    address:  str
    created_at:  datetime