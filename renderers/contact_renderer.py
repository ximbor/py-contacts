from abc import ABC, abstractmethod
from typing import List

from models.contact import Contact

class ContactRenderer(ABC):

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def display(self, contact: Contact) -> None:
        pass

    @abstractmethod
    def display_many(self, contacts: List[Contact]) -> None:
        pass