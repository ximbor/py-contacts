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