from typing import List, Optional

from sqlalchemy.orm import Session

from src.adapters_logic.dtos.client_dto import ClientDTO
from src.adapters_logic.mappers.client_mapper import (
    client_to_dto,
)
from src.alchemy_db.repositories import clients_repository


class ClientService:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, dto: ClientDTO) -> ClientDTO:
        client = clients_repository.create_client(
            db=self.db,
            name=dto.name,
            email=dto.email,
            phone_number=dto.phone_number,
            address=dto.address,
            created_at=dto.created_at,
        )

        return client_to_dto(client)

    def get_client_by_id(self, client_id: int) -> Optional[ClientDTO]:
        client = clients_repository.get_client_by_id(
            db=self.db,
            client_id=client_id,
        )

        if not client:
            return None

        return client_to_dto(client)

    def get_client_by_email(self, email: str) -> Optional[ClientDTO]:
        client = clients_repository.get_client_by_email(
            db=self.db,
            email=email,
        )

        if not client:
            return None

        return client_to_dto(client)

    def get_all_clients(self) -> List[ClientDTO]:
        clients = clients_repository.get_all_clients(self.db)

        return [client_to_dto(client) for client in clients]

    def update_client(
        self,
        client_id: int,
        dto: ClientDTO
    ) -> Optional[ClientDTO]:
        client = clients_repository.update_client(
            db=self.db,
            client_id=client_id,
            name=dto.name,
            email=dto.email,
            phone_number=dto.phone_number,
            address=dto.address,
        )

        if not client:
            return None

        return client_to_dto(client)

    def delete_client(self, client_id: int) -> bool:
        return clients_repository.delete_client(
            db=self.db,
            client_id=client_id,
        )