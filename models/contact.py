from dataclasses import dataclass
from typing import Tuple
from .address import Address

@dataclass
class Contact:
    """
    Contact class.

    Attributes:
        first_name (str): First name.
        last_name (str): Last name.
        email (str): Email address.
        address (Address): Address.
        phone_numbers (List[PhoneNumber]): List of phone numbers.
        tags (List[Tag]): List of tags.
    """

    first_name: str
    last_name: str
    email: str
    address: Address
    phone_numbers: Tuple[str]
    tags: Tuple[str]

    @staticmethod
    def from_dict(data: dict) -> 'Contact':
        """
        Converts data from dictionary to Contact.

        Args:
            data (dict): Dictionary data representing a contact.

        Returns:
            Contact: contact.
        """
        return Contact(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            address=Address(**data["address"]),
            phone_numbers=tuple(data["phone_numbers"]),
            tags=tuple(data["tags"]),
        )