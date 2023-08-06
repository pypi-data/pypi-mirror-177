from typing import Mapping, Any

ISSUE_TYPE = int
ISSUE_TYPE_TASK: ISSUE_TYPE = 0
ISSUE_TYPE_BUG: ISSUE_TYPE = 1

ISSUE_STATE = int
ISSUE_STATE_PLAN: ISSUE_STATE = 0
ISSUE_STATE_PROCESS: ISSUE_STATE = 1
ISSUE_STATE_CHECK: ISSUE_STATE = 2
ISSUE_STATE_CLOSE: ISSUE_STATE = 3


class CreateEvent:  # 创建issue
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title


class UpdateEvent:  # 更新issue
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, old_title: str = "", new_title="", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.old_title = old_title
        self.new_title = new_title


class RemoveEvent:  # 删除issue
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title


class AssignExecUserEvent:  # 指派执行者
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", exec_user_id: str = "",
                 exec_user_display_name: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.exec_user_id = exec_user_id
        self.exec_user_display_name = exec_user_display_name


class AssignCheckUserEvent:  # 指派检查者
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "",
                 check_user_id: str = "", check_user_display_name: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.check_user_id = check_user_id
        self.check_user_display_name = check_user_display_name


class ChangeStateEvent:  # 修改状态
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "",
                 old_state: ISSUE_STATE = ISSUE_STATE_PLAN, new_state: ISSUE_STATE = ISSUE_STATE_PLAN,  **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.old_state = old_state
        self.new_state = new_state


class LinkSpritEvent:  # 关联到迭代
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "",
                 sprit_id: str = "", sprit_title: str = "",  **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.sprit_id = sprit_id
        self.sprit_title = sprit_title


class SetStartTimeEvent:  # 设置开始时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", start_time: int = 0, **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.start_time = start_time


class CancelStartTimeEvent:  # 取消开始时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title


class SetEndTimeEvent:  # 设置结束时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", end_time: int = 0, **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.end_time = end_time


class CancelEndTimeEvent:  # 取消结束时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title


class SetEstimateMinutesEvent:  # 设置预估时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", estimate_minutes: int = 0, **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.estimate_minutes = estimate_minutes


class CancelEstimateMinutesEvent:  # 取消预估时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title


class SetRemainMinutesEvent:  # 设置剩余时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "",
                 remain_minutes: int = 0, has_spend_minutes: bool = False, spend_minutes: int = 0, **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title
        self.remain_minutes = remain_minutes
        self.has_spend_minutes = has_spend_minutes
        self.spend_minutes = spend_minutes


class CancelRemainMinutesEvent:  # 取消剩余时间
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.title = title


class CreateSubIssueEvent:  # 增加子工单
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, issue_title: str = "", title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.issue_title = issue_title
        self.title = title


class UpdateSubIssueEvent:  # 更新子工单
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, issue_title: str = "",
                 old_title: str = "", new_title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.issue_title = issue_title
        self.old_title = old_title
        self.new_title = new_title


class UpdateSubIssueStateEvent:  # 更新子工单状态
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, issue_title: str = "", title: str = "", done: bool = False, **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.issue_title = issue_title
        self.title = title
        self.done = done


class RemoveSubIssueEvent:  # 删除子工单
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, issue_title: str = "", title: str = "", **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.issue_title = issue_title
        self.title = title


class AddDependenceEvent:  # 增加依赖
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, issue_title: str = "",
                 depend_issue_id: str = "", depend_issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, depend_issue_title: str = "",
                 **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.issue_title = issue_title
        self.depend_issue_id = depend_issue_id
        self.depend_issue_type = depend_issue_type
        self.depend_issue_title = depend_issue_title


class RemoveDependenceEvent:  # 删除依赖
    def __init__(self, issue_id: str = "", issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, issue_title: str = "",
                 depend_issue_id: str = "", depend_issue_type: ISSUE_TYPE = ISSUE_TYPE_TASK, depend_issue_title: str = "",
                 **param):
        self.issue_id = issue_id
        self.issue_type = issue_type
        self.issue_title = issue_title
        self.depend_issue_id = depend_issue_id
        self.depend_issue_type = depend_issue_type
        self.depend_issue_title = depend_issue_title


IssueEvents = CreateEvent | UpdateEvent | RemoveEvent | AssignExecUserEvent | AssignCheckUserEvent | ChangeStateEvent | LinkSpritEvent | SetStartTimeEvent | CancelStartTimeEvent | SetEndTimeEvent | CancelEndTimeEvent | SetEstimateMinutesEvent | CancelEstimateMinutesEvent | SetRemainMinutesEvent | CancelRemainMinutesEvent | CreateSubIssueEvent | UpdateSubIssueEvent | UpdateSubIssueStateEvent | RemoveSubIssueEvent | AddDependenceEvent | RemoveDependenceEvent | None

def parseIssueEvent(ev: Mapping[str, Mapping[str, Any]]) -> IssueEvents:
    if "CreateEvent" in ev:
        return CreateEvent(**ev["CreateEvent"])
    elif "UpdateEvent" in ev:
        return UpdateEvent(**ev["UpdateEvent"])
    elif "RemoveEvent" in ev:
        return RemoveEvent(**ev["RemoveEvent"])
    elif "AssignExecUserEvent" in ev:
        return AssignExecUserEvent(**ev["AssignExecUserEvent"])
    elif "AssignCheckUserEvent" in ev:
        return AssignCheckUserEvent(**ev["AssignCheckUserEvent"])
    elif "ChangeStateEvent" in ev:
        return ChangeStateEvent(**ev["ChangeStateEvent"])
    elif "LinkSpritEvent" in ev:
        return LinkSpritEvent(**ev["LinkSpritEvent"])
    elif "SetStartTimeEvent" in ev:
        return SetStartTimeEvent(**ev["SetStartTimeEvent"])
    elif "CancelStartTimeEvent" in ev:
        return CancelStartTimeEvent(**ev["CancelStartTimeEvent"])
    elif "SetEndTimeEvent" in ev:
        return SetEndTimeEvent(**ev["SetEndTimeEvent"])
    elif "CancelEndTimeEvent" in ev:
        return CancelEndTimeEvent(**ev["CancelEndTimeEvent"])
    elif "SetEstimateMinutesEvent" in ev:
        return SetEstimateMinutesEvent(**ev["SetEstimateMinutesEvent"])
    elif "CancelEstimateMinutesEvent" in ev:
        return CancelEstimateMinutesEvent(**ev["CancelEstimateMinutesEvent"])
    elif "SetRemainMinutesEvent" in ev:
        return SetRemainMinutesEvent(**ev["SetRemainMinutesEvent"])
    elif "CancelRemainMinutesEvent" in ev:
        return CancelRemainMinutesEvent(**ev["CancelRemainMinutesEvent"])
    elif "CreateSubIssueEvent" in ev:
        return CreateSubIssueEvent(**ev["CreateSubIssueEvent"])
    elif "UpdateSubIssueEvent" in ev:
        return UpdateSubIssueEvent(**ev["UpdateSubIssueEvent"])
    elif "UpdateSubIssueStateEvent" in ev:
        return UpdateSubIssueStateEvent(**ev["UpdateSubIssueStateEvent"])
    elif "RemoveSubIssueEvent" in ev:
        return RemoveSubIssueEvent(**ev["RemoveSubIssueEvent"])
    elif "AddDependenceEvent" in ev:
        return AddDependenceEvent(**ev["AddDependenceEvent"])
    elif "RemoveDependenceEvent" in ev:
        return RemoveDependenceEvent(**ev["RemoveDependenceEvent"])
    else:
        return None