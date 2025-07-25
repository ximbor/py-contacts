from abc import ABC, abstractmethod
from typing import List

from models.contact import Contact

class ContactRenderer(ABC):
    """
    Contact renderer interface.
    """

    @abstractmethod
    def render(self) -> str:
        """
        Renders a contact.
        Returns:
             The rendered contact.
        """
        pass

    @abstractmethod
    def display(self, contact: Contact) -> None:
        """
        Displays a contact.
        Returns:
             None.
        """
        pass

    @abstractmethod
    def display_many(self, contacts: List[Contact]) -> None:
        """
        Displays a list of contacts.
        Returns:
             None.
        """
        pass