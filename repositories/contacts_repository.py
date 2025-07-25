from abc import ABC, abstractmethod
from typing import List

from models.contact import Contact

class ContactsRepository(ABC):
    """
    Contacts repository interface.
    """

    @abstractmethod
    def load_all(self) -> None:
        """
        Loads all contacts.

        Returns:
             List[Contact]: Contacts list.
        """
        pass

    @abstractmethod
    def upsert(self, contact: Contact) -> Contact:
        """
        Upserts a contact.
        Args:
             contact (Contact): Contact.
        Returns:
            Contact: upserted contact.
        """
        pass

    @abstractmethod
    def delete(self, first_name, last_name) -> None:
        """
        Deletes a contact.

        Args:
             first_name (str): First name.
             last_name (str): Last name.

        Returns:
            None.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Contact]:
        """
        Gets all contacts.
        Returns:
            List[Contact]: Contacts list.
        """
        pass

    @abstractmethod
    def export(self, export_path: str) -> None:
        """
        Exports all contacts.
        Args:
            export_path (str): Path to export file.
        Returns:
            None.
        """
        pass

    @abstractmethod
    def search(self, first_name = None, last_name = None) -> list[Contact]:
        """
        Search for contacts.

        Args:
            first_name (str): First name.
            last_name (str): Last name.

        Returns:
            List[Contact]: Contacts list.
        """
        pass