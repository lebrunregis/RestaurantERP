from typing import Optional

from src.adapters_logic.dtos.client_dto import ClientDTO
from src.alchemy_db.models.clients_model import Client


def client_to_dto(client: Client) -> ClientDTO:
    return ClientDTO(
        client_id=client.client_id,
        name=client.name,
        email=client.email,
        phone_number=client.phone_number,
        address=client.address,
        created_at=client.created_at,
    )


def dto_to_client(
    dto: ClientDTO,
    client: Optional[Client] = None
) -> Client:

    if client is None:
        client = Client()

    client.client_id = dto.client_id
    client.name = dto.name
    client.email = dto.email
    client.phone_number = dto.phone_number
    client.address = dto.address
    client.created_at = dto.created_at

    return client