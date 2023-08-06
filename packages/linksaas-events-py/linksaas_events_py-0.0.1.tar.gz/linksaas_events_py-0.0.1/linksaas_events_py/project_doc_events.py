from typing import Mapping, Any


class CreateSpaceEvent:  # 创建文档空间
    def __init__(self, doc_space_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.title = title


class UpdateSpaceEvent:  # 修改文档空间
    def __init__(self, doc_space_id: str = "", old_title: str = "", new_title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.old_title = old_title
        self.new_title = new_title


class RemoveSpaceEvent:  # 删除文档空间
    def __init__(self, doc_space_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.title = title


class CreateDocEvent:  # 创建文档
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id
        self.title = title


class UpdateDocEvent:  # 更新文档 (同一个用户同一个文档修改，不记录一个小时内的操作)
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", old_title: str = "", new_title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id
        self.old_title = old_title
        self.new_title = new_title


class MoveDocToRecycleEvent:  # 移动到回收站
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id
        self.title = title


class RemoveDocEvent:  # 删除文档
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id


class RecoverDocEvent:  # 恢复文档
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id
        self.title = title


class WatchDocEvent:  # 关注文档
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id
        self.title = title


class UnWatchDocEvent:  # 取消关注文档
    def __init__(self, doc_space_id: str = "", doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.doc_space_id = doc_space_id
        self.doc_space_name = doc_space_name
        self.doc_id = doc_id
        self.title = title


class MoveDocEvent:  # 移动文档
    def __init__(self, src_doc_space_id: str = "", src_doc_space_name: str = "", dest_doc_space_id: str = "",
                 dest_doc_space_name: str = "", doc_id: str = "", title: str = "", **params):
        self.src_doc_space_id = src_doc_space_id
        self.src_doc_space_name = src_doc_space_name
        self.dest_doc_space_id = dest_doc_space_id
        self.dest_doc_space_name = dest_doc_space_name
        self.doc_id = doc_id
        self.title = title


DocEvents = CreateSpaceEvent | UpdateSpaceEvent | RemoveSpaceEvent | CreateDocEvent | UpdateDocEvent | MoveDocToRecycleEvent | \
    RemoveDocEvent | RecoverDocEvent | WatchDocEvent | UnWatchDocEvent | MoveDocEvent | None


def parseDocEvent(ev: Mapping[str, Mapping[str, Any]]) -> DocEvents:
    if "CreateSpaceEvent" in ev:
        return CreateSpaceEvent(**ev["CreateSpaceEvent"])
    elif "UpdateSpaceEvent" in ev:
        return UpdateSpaceEvent(**ev["UpdateSpaceEvent"])
    elif "RemoveSpaceEvent" in ev:
        return RemoveSpaceEvent(**ev["RemoveSpaceEvent"])
    elif "CreateDocEvent" in ev:
        return CreateDocEvent(**ev["CreateDocEvent"])
    elif "UpdateDocEvent" in ev:
        return UpdateDocEvent(**ev["UpdateDocEvent"])
    elif "MoveDocToRecycleEvent" in ev:
        return MoveDocToRecycleEvent(**ev["MoveDocToRecycleEvent"])
    elif "RemoveDocEvent" in ev:
        return RemoveDocEvent(**ev["RemoveDocEvent"])
    elif "RecoverDocEvent" in ev:
        return RecoverDocEvent(**ev["RecoverDocEvent"])
    elif "WatchDocEvent" in ev:
        return WatchDocEvent(**ev["WatchDocEvent"])
    elif "UnWatchDocEvent" in ev:
        return UnWatchDocEvent(**ev["UnWatchDocEvent"])
    elif "MoveDocEvent " in ev:
        return MoveDocEvent(**ev["MoveDocEvent"])
    else:
        return None
