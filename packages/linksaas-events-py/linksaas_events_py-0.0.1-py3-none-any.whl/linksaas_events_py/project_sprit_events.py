from typing import Mapping, Any


class CreateEvent:  # 创建迭代
    def __init__(self, sprit_id: str = "", title: str = "", **param):
        self.sprit_id = sprit_id
        self.title = title


class UpdateEvent:  # 更新迭代
    def __init__(self, sprit_id: str = "", old_title: str = "", new_title: str = "", **param):
        self.sprit_id = sprit_id
        self.old_title = old_title
        self.new_title = new_title


SpritEvents = CreateEvent | UpdateEvent | None


def parseSpritEvent(ev: Mapping[str, Mapping[str, Any]]) -> SpritEvents:
    if "CreateEvent" in ev:
        return CreateEvent(**ev["CreateEvent"])
    elif "UpdateEvent" in ev:
        return UpdateEvent(**ev["UpdateEvent"])
    else:
        return None
