from typing import Tuple, List

from models.address import Address
from models.contact import Contact
from renderers.contact_renderer import ContactRenderer

class TextContactRenderer(ContactRenderer):

    def __init__(self):
        self.CONTACT_SEPARATOR = "=" * 50
        self.TITLE_SEPARATOR = ": "
        self.padding = 15
        self.header = self.CONTACT_SEPARATOR
        self.footer = self.CONTACT_SEPARATOR

    @staticmethod
    def _build_address(address: Address) -> str:
        return f"{address.street_location} , {address.city}, {address.state}, {address.zipcode}"

    @staticmethod
    def _build__string_tuple(values: Tuple[str], indentation: int) -> str:
        if len(values) == 0: return ""
        return f"• {f"\n{" " * indentation}• ".join(values)}"

    def _with_padding(self, text: str) -> str:
        length = self.padding
        if len(text) > length:
            return text[:length]
        padding_string = " " * (length - len(text))
        return text + padding_string

    def _build_line(self, title:str, value:str) -> str:
        return f"{self._with_padding(title)}{self.TITLE_SEPARATOR}{value}"

    def render(self, contact: Contact):
        return f"""
{self._build_line("First name", contact.first_name)}
{self._build_line("Last name", contact.last_name)}
{self._build_line("E-mail", contact.email)}
{self._build_line("phone numbers", TextContactRenderer._build__string_tuple(contact.phone_numbers, self.padding + len(self.TITLE_SEPARATOR)))}
{self._build_line("Address", TextContactRenderer._build_address(contact.address))}
{self._build_line("Tags", TextContactRenderer._build__string_tuple(contact.tags, self.padding + len(self.TITLE_SEPARATOR)))}
"""

    def display(self, contact: Contact):
        print(self.render(contact))

    def display_many(self, contacts: List[Contact]):
        rendered_contacts = ""
        for contact in contacts:
            rendered_contacts += self.header + self.render(contact)
        rendered_contacts + self.footer
        print(rendered_contacts)