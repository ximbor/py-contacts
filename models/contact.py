from dataclasses import dataclass
from typing import Tuple
from .address import Address

@dataclass
class Contact:
    first_name: str
    last_name: str
    email: str
    address: Address
    phone_numbers: Tuple[str]
    tags: Tuple[str]

    @staticmethod
    def from_dict(data: dict) -> 'Contact':
        return Contact(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            address=Address(**data["address"]),
            phone_numbers=tuple(data["phone_numbers"]),
            tags=tuple(data["tags"]),
        )