from typing import List, Optional

from sqlalchemy.orm import Session

from src.adapters_logic.dtos.client_dto import ClientDTO
from src.adapters_logic.mappers.client_mapper import (
    client_to_dto,
)
from src.alchemy_db.repositories import clients_repository



def create_client(db: Session, dto: ClientDTO) -> ClientDTO:
        client = clients_repository.create_client(
            db=db,
            name=dto.name,
            email=dto.email,
            phone_number=dto.phone_number,
            address=dto.address,
            created_at=dto.created_at,
        )

        return client_to_dto(client)

def get_client_by_id(db: Session, client_id: int) -> Optional[ClientDTO]:
        client = clients_repository.get_client_by_id(
            db=db,
            client_id=client_id,
        )

        if not client:
            return None

        return client_to_dto(client)

def get_client_by_email(db: Session, email: str) -> Optional[ClientDTO]:
        client = clients_repository.get_client_by_email(
            db=db,
            email=email,
        )

        if not client:
            return None

        return client_to_dto(client)

def get_all_clients(db: Session) -> List[ClientDTO]:
        clients = clients_repository.get_all_clients(db)

        return [client_to_dto(client) for client in clients]

def get_clients_paginated(db: Session, page: int = 1, per_page: int = 50) -> List[ClientDTO]:
        clients = clients_repository.get_clients_paginated(db, page, per_page)

        return [client_to_dto(client) for client in clients]

def get_clients_containing_in_name (db: Session, substr: str)-> list[ClientDTO]:
  clients =   clients_repository.get_clients_containing_in_name(db, substr)
  return [client_to_dto(r) for r in clients]
  
def get_clients_containing_in_name_paginated (db: Session, substr: str, page: int = 1, per_page: int = 50)-> list[RecipeDTO]:
    clients =   clients_repository.get_clients_containing_in_name_paginated(db, substr,  page, per_page)
    return [client_to_dto(r) for r in clients]

def update_client(
        db: Session,
        client_id: int,
        dto: ClientDTO
    ) -> Optional[ClientDTO]:
        client = clients_repository.update_client(
            db=db,
            client_id=client_id,
            name=dto.name,
            email=dto.email,
            phone_number=dto.phone_number,
            address=dto.address,
        )

        if not client:
            return None

        return client_to_dto(client)

def delete_client(db: Session, client_id: int) -> bool:
        return clients_repository.delete_client(
            db=db,
            client_id=client_id,
        )

def count_clients(db: Session)-> int:
              return clients_repository.count_clients(
            db=db,
        )