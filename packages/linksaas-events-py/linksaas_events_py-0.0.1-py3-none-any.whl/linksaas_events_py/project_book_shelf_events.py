
from typing import Mapping, Any


class AddBookEvent:  # 增加书本
    def __init__(self, book_id: str = "", book_title: str = "", **params):
        self.book_id = book_id
        self.book_title = book_title


class RemoveBookEvent:  # 删除书本
    def __init__(self, book_id: str = "", book_title: str = "", **params):
        self.book_id = book_id
        self.book_title = book_title


BookShelfEvents = AddBookEvent | RemoveBookEvent | None


def parseBookShelfEvent(ev: Mapping[str, Mapping[str, Any]]) -> BookShelfEvents:
    if "AddBookEvent" in ev:
        return AddBookEvent(**ev["AddBookEvent"])
    elif "RemoveBookEvent" in ev:
        return RemoveBookEvent(**ev["RemoveBookEvent"])
    else:
        return None
