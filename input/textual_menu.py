from typing import List

from input.menu import Menu
from input.menu_item import MenuItem


class TextualMenu(Menu):

    def __init__(self, items: List[MenuItem]):
        self.items = items

    def display(self) -> None:
        for item in self.items:
           print(f"""{item.key}. {item.text}""")