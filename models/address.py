from dataclasses import dataclass
from typing import Tuple

@dataclass
class Address:
    """
    Address class.

    Attributes:
        street_location (str): Street location of the address.
        city (str): City of the address.
        state (str): State of the address.
        zipcode (str): Zip code of the address.
    """
    street_location: str
    city: str
    state: str
    zipcode: str