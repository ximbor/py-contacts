from typing import Tuple, List

from IPython.display import display, HTML

from models.address import Address
from models.contact import Contact
from renderers.contact_renderer import ContactRenderer

class HtmlContactRenderer(ContactRenderer):

    def __init__(self):
        self.CONTACT_SEPARATOR = "<hr/>"
        self.TITLE_SEPARATOR = ": "
        self.PADDING = 15
        self.HEADER = self.CONTACT_SEPARATOR
        self.FOOTER = self.CONTACT_SEPARATOR

    @staticmethod
    def _build_address(address: Address) -> str:
        return f"{address.street_location} , {address.city}, {address.state}, {address.zipcode}"

    @staticmethod
    def _build_string_tuple(values: Tuple[str]) -> str:
        if len(values) == 0: return ""
        values_str = ""
        for value in values:
            values_str += f"<li>{value}</li>"
        return values_str

    @staticmethod
    def _build_tag_tuple(values: Tuple[str]) -> str:
        if len(values) == 0: return ""
        values_str = ""
        for value in values:
            values_str += f"""<span style="background: #e0f7fa; border-radius: 4px; padding: 2px 6px; margin-right: 4px;">{value}</span>"""
        return values_str

    def _build_line(self, title:str, value:str) -> str:
        return f"<div><strong>{title}{self.TITLE_SEPARATOR}</strong> {value}</div>"

    def render(self, contact: Contact):
        html = f"""
            <div style="border: 1px solid #ccc; border-radius: 10px; padding: 16px; max-width: 500px; font-family: sans-serif;">              
              {self._build_line("👤 First name", contact.first_name)}
              {self._build_line("👤 Last name", contact.last_name)}
              {self._build_line("📧 Email", contact.email)}
              <div><strong>📞 Phone numbers{self.TITLE_SEPARATOR}</strong>
                <ul style="margin: 4px 0 10px 20px; padding: 0;">
                  {self._build_string_tuple(contact.phone_numbers)}
                </ul>
              </div>
              {self._build_line("📍 Address",self._build_address(contact.address))}

              <div><strong>🏷️ Tags:</strong>
                {HtmlContactRenderer._build_tag_tuple(contact.tags)}
              </div>
            </div>
        """
        return html

    def display(self, contact: Contact):
        display(HTML(self.render(contact)))

    def display_many(self, contacts: List[Contact]):
        display(HTML(self.FOOTER))
        for contact in contacts:
            self.display(contact)
        display(HTML(self.FOOTER))