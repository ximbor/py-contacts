from typing import Callable


class MenuItem:
    """
    Menu item class.
    """

    def __init__(self, key: int, code: str, text: str, action: Callable) -> None:
        self.key = key
        self.code = code
        self.text = text
        self.action = action