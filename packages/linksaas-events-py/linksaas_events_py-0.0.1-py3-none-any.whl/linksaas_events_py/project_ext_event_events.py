from typing import Mapping, Any

EVENT_SOURCE = int
EVENT_SOURCE_GITLAB: EVENT_SOURCE = 0
EVENT_SOURCE_GITHUB: EVENT_SOURCE = 1
EVENT_SOURCE_GITEA: EVENT_SOURCE = 2
EVENT_SOURCE_GITEE: EVENT_SOURCE = 3
EVENT_SOURCE_GOGS: EVENT_SOURCE = 4
EVENT_SOURCE_JIRA: EVENT_SOURCE = 5
EVENT_SOURCE_CONFLUENCE: EVENT_SOURCE = 6
EVENT_SOURCE_JENKINS: EVENT_SOURCE = 7


SOURCE_USER_POLICY = int
SOURCE_USER_POLICY_NONE: SOURCE_USER_POLICY = 0  # 未设置策略
SOURCE_USER_POLICY_DISCARD: SOURCE_USER_POLICY = 1  # 丢弃事件
SOURCE_USER_POLICY_MAPPING: SOURCE_USER_POLICY = 2  # 映射用户
SOURCE_USER_POLICY_SKIP_MAPPING: SOURCE_USER_POLICY = 3  # 跳过用户映射环节


class CreateEvent:  # 创建事件源
    def __init__(self, event_source_id: str = "", event_source: EVENT_SOURCE = EVENT_SOURCE_GITLAB, title: str = "", **params):
        self.event_source_id = event_source_id
        self.event_source = event_source
        self.title = title


class UpdateEvent:  # 更新事件源
    def __init__(self, event_source_id: str = "", event_source: EVENT_SOURCE = EVENT_SOURCE_GITLAB, old_title: str = "", new_title: str = "", **params):
        self.event_source_id = event_source_id
        self.event_source = event_source
        self.old_title = old_title
        self.new_title = new_title


class GetSecretEvent:  # 获取事件源秘钥
    def __init__(self, event_source_id: str = "", event_source: EVENT_SOURCE = EVENT_SOURCE_GITLAB, title: str = "", **params):
        self.event_source_id = event_source_id
        self.event_source = event_source
        self.title = title


class RemoveEvent:  # 删除事件源
    def __init__(self, event_source_id: str = "", event_source: EVENT_SOURCE = EVENT_SOURCE_GITLAB, title: str = "", **params):
        self.event_source_id = event_source_id
        self.event_source = event_source
        self.title = title


class SetSourceUserPolicyEvent:  # 设置事件源用户策略
    def __init__(self, event_source_id: str = "", event_source: EVENT_SOURCE = EVENT_SOURCE_GITLAB, title: str = "", source_user_name: str = "",
                 source_display_name: str = "", user_policy: SOURCE_USER_POLICY = SOURCE_USER_POLICY_NONE, map_user_id: str = "",
                 map_user_display_name: str = "", **params):
        self.event_source_id = event_source_id
        self.event_source = event_source
        self.title = title
        self.source_user_name = source_user_name
        self.source_display_name = source_display_name
        self.user_policy = user_policy
        self.map_user_id = map_user_id
        self.map_user_display_name = map_user_display_name


ExtEvents = CreateEvent | UpdateEvent | GetSecretEvent | RemoveEvent | SetSourceUserPolicyEvent | None


def parseExtEvent(ev: Mapping[str, Mapping[str, Any]]) -> ExtEvents:
    if "CreateEvent" in ev:
        return CreateEvent(**ev["CreateEvent"])
    elif "UpdateEvent" in ev:
        return UpdateEvent(**ev["UpdateEvent"])
    elif "GetSecretEvent" in ev:
        return GetSecretEvent(**ev["GetSecretEvent"])
    elif "RemoveEvent" in ev:
        return RemoveEvent(**ev["RemoveEvent"])
    elif "SetSourceUserPolicyEvent" in ev:
        return SetSourceUserPolicyEvent(**ev["SetSourceUserPolicyEvent"])
    else:
        return None
