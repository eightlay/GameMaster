from telegram.ext import MessageFilter
from telegram import Message


class CustomFilters:
    """Custom telegram filters"""

    class PositiveInteger(MessageFilter):
        name = "positive_int"

        def filter(self, message: Message) -> bool:
            try:
                return int(message.text) > 0
            except ValueError:
                return False

    positive_int = PositiveInteger()

    class TextLenUBound():
        name = "text_len_ubound"

        def __call__(self, ubound: int) -> MessageFilter:
            def filter(message: Message) -> bool:
                try:
                    return int(message.text) <= ubound
                except ValueError:
                    return False

    text_len_ubound = TextLenUBound()