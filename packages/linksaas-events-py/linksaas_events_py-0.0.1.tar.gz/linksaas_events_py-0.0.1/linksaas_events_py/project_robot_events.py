from typing import Mapping, Any

class CreateEvent:  # 创建机器人
    def __init__(self, robot_id: str = "", robot_name: str = "", **param):
        robot_id = robot_id
        robot_name = robot_name


class UpdateEvent:  # 更新机器人
    def __init__(self, robot_id: str = "", old_robot_name: str = "", new_robotname: str = "", **param):
        robot_id = robot_id
        old_robot_name = old_robot_name
        new_robotname = new_robotname


class RemoveEvent:  # 删除机器人
    def __init__(self, robot_id: str = "", robot_name: str = "", **param):
        robot_id = robot_id
        robot_name = robot_name


class AddAccessUserEvent:  # 新增访问用户
    def __init__(self, robot_id: str = "", robot_name: str = "", member_user_id: str = "", member_display_name: str = "", **param):
        robot_id = robot_id
        robot_name = robot_name
        member_user_id = member_user_id
        member_display_name = member_display_name


class RemoveAccessUserEvent:  # 删除访问用户
    def __init__(self, robot_id: str = "", robot_name: str = "", member_user_id: str = "", member_display_name: str = "", **param):
        robot_id = robot_id
        robot_name = robot_name
        member_user_id = member_user_id
        member_display_name = member_display_name


class RenewTokenEvent:  # 更新访问令牌
    def __init__(self, robot_id: str = "", robot_name: str = "", **param):
        robot_id = robot_id
        robot_name = robot_name

RobotEvents = CreateEvent|UpdateEvent|RemoveEvent|AddAccessUserEvent|RemoveAccessUserEvent|RenewTokenEvent|None

def parseRobotEvent(ev: Mapping[str, Mapping[str, Any]]) -> RobotEvents:
    if "CreateEvent" in ev:
        return CreateEvent(**ev["CreateEvent"])
    elif "UpdateEvent" in ev:
        return UpdateEvent(**ev["UpdateEvent"])
    elif "RemoveEvent" in ev:
        return RemoveEvent(**ev["RemoveEvent"])
    elif "AddAccessUserEvent" in ev:
        return AddAccessUserEvent(**ev["AddAccessUserEvent"])
    elif "RemoveAccessUserEvent" in ev:
        return RemoveAccessUserEvent(**ev["RemoveAccessUserEvent"])
    elif "RenewTokenEvent" in ev:
        return RenewTokenEvent(**ev["RenewTokenEvent"])
    else:
        return None