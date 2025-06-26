from abc import ABC, abstractmethod
from typing import List

from models.contact import Contact

class ContactsRepository(ABC):

    @abstractmethod
    def load_all(self) -> None:
        pass

    @abstractmethod
    def upsert(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def delete(self, first_name, last_name) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Contact]:
        pass

    @abstractmethod
    def export(self, export_path: str) -> None:
        pass

    @abstractmethod
    def search(self, first_name = None, last_name = None) -> list[Contact]:
        pass