from dataclasses import dataclass
from typing import Tuple

@dataclass
class Address:
    street_location: str
    city: str
    state: str
    zipcode: str