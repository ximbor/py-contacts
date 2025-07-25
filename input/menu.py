from abc import ABC


class Menu(ABC):
    """
    Menu interface.
    """

    def display(self) -> None:
        """
        Display the menu.
        """
        pass