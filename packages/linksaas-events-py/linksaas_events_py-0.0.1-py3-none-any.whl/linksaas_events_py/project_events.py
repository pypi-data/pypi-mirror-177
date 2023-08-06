from typing import Mapping, Any

APP_OPEN_TYPE = int
OPEN_TYPE_BROWSER: APP_OPEN_TYPE = 0
OPEN_TYPE_INNER: APP_OPEN_TYPE = 1


class CreateProjectEvent:  # 创建项目
    pass


class UpdateProjectEvent:  # 设置项目
    def __init__(self, new_project_name: str = "", **params):
        # 项目名称
        self.new_project_name = new_project_name


class OpenProjectEvent:  # 打开项目
    pass


class CloseProjectEvent:  # 关闭项目
    pass


class RemoveProjectEvent:  # 删除项目
    pass


class GenInviteEvent:  # 创建邀请码
    pass


class JoinProjectEvent:  # 加入项目
    pass


class LeaveProjectEvent:  # 离开项目
    pass


class CreateRoleEvent:  # 创建角色
    def __init__(self, role_id: str = "", role_name: str = "", **params):
        self.role_id = role_id
        self.role_name = role_name


class UpdateRoleEvent:  # 更新角色
    def __init__(self, role_id: str = "", old_role_name: str = "", new_role_name: str = "", **params):
        self.role_id = role_id
        self.old_role_name = old_role_name
        self.new_role_name = new_role_name


class RemoveRoleEvent:  # 删除角色
    def __init__(self, role_id: str = "", role_name: str = "", **params):
        self.role_id = role_id
        self.role_name = role_name


class UpdateProjectMemberEvent:  # 更新成员
    def __init__(self, member_user_id: str = "", old_member_display_name: str = "", new_member_display_name: str = "", **params):
        self.member_user_id = member_user_id
        self.old_member_display_name = old_member_display_name
        self.new_member_display_name = new_member_display_name


class RemoveProjectMemberEvent:  # 删除成员
    def __init__(self, member_user_id: str = "", member_display_name: str = "", **params):
        self.member_user_id = member_user_id
        self.member_display_name = member_display_name


class SetProjectMemberRoleEvent:  # 设置成员角色
    def __init__(self, role_id: str = "", role_name: str = "", member_user_id: str = "", member_display_name: str = "", **params):
        self.role_id = role_id
        self.role_name = role_name
        self.member_user_id = member_user_id
        self.member_display_name = member_display_name


class UploadWorkSnapShotEvent:  # 工作快照
    def __init__(self, fs_id: str = "", file_id: str = "", thumb_file_id: str = "", **params):
        self.fs_id = fs_id
        self.file_id = file_id
        self.thumb_file_id = thumb_file_id


class CreateChannelEvent:  # 创建频道
    def __init__(self, channel_id: str = "", channel_name: str = "", pub_channel: bool = False, **params):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.pub_channel = pub_channel


class UpdateChannelEvent:  # 更新频道
    def __init__(self, channel_id: str = "", old_channel_name: str = "", old_pub_channel: bool = False, new_channel_name: str = "", new_pub_channel: bool = False, **params):
        self.channel_id = channel_id
        self.old_channel_name = old_channel_name
        self.old_pub_channel = old_pub_channel
        self.new_channel_name = new_channel_name
        self.new_pub_channel = new_pub_channel


class OpenChannelEvent:  # 打开频道
    def __init__(self, channel_id: str = "", channel_name: str = "", **params):
        self.channel_id = channel_id
        self.channel_name = channel_name


class CloseChannelEvent:  # 关闭频道
    def __init__(self, channel_id: str = "", channel_name: str = "", **params):
        self.channel_id = channel_id
        self.channel_name = channel_name


class RemoveChannelEvent:  # 删除频道
    def __init__(self, channel_id: str = "", channel_name: str = "", **params):
        self.channel_id = channel_id
        self.channel_name = channel_name


class AddChannelMemberEvent:  # 增加频道成员
    def __init__(self, channel_id: str = "", channel_name: str = "", member_user_id: str = "", member_display_name: str = "", **params):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.member_user_id = member_user_id
        self.member_display_name = member_display_name


class RemoveChannelMemberEvent:  # 删除频道成员
    def __init__(self, channel_id: str = "", channel_name: str = "", member_user_id: str = "", member_display_name: str = "", **params):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.member_user_id = member_user_id
        self.member_display_name = member_display_name


class CreateAppraiseEvent:  # 创建评估
    def __init__(self, appraise_id: str = "", title: str = "", **params):
        self.appraise_id = appraise_id
        self.title = title


class AddProjectAppEvent:  # 增加项目应用
    def __init__(self, app_id: str = "", app_name: str = "", app_url: str = "", app_open_type: APP_OPEN_TYPE = OPEN_TYPE_BROWSER, **params):
        self.app_id = app_id
        self.app_name = app_name
        self.app_url = app_url
        self.app_open_type = app_open_type


class RemoveProjectAppEvent:  # 删除项目应用
    def __init__(self, app_id: str = "", app_name: str = "", **params):
        self.app_id = app_id
        self.app_name = app_name


ProjectEvents = CreateProjectEvent | UpdateProjectEvent | OpenProjectEvent | CloseProjectEvent | RemoveProjectEvent | GenInviteEvent | JoinProjectEvent | LeaveProjectEvent | CreateRoleEvent | UpdateRoleEvent | RemoveRoleEvent | UpdateProjectMemberEvent | RemoveProjectMemberEvent | SetProjectMemberRoleEvent | UploadWorkSnapShotEvent | CreateChannelEvent | UpdateChannelEvent | OpenChannelEvent | CloseChannelEvent | RemoveChannelEvent | AddChannelMemberEvent | RemoveChannelMemberEvent | CreateAppraiseEvent | AddProjectAppEvent | RemoveProjectAppEvent | None


def parseProjectEvent(ev: Mapping[str, Mapping[str, Any]]) -> ProjectEvents:
    if "CreateProjectEvent" in ev:
        return CreateProjectEvent()
    elif "UpdateProjectEvent" in ev:
        return UpdateProjectEvent(**ev["UpdateProjectEvent"])
    elif "OpenProjectEvent" in ev:
        return OpenProjectEvent()
    elif "CloseProjectEvent" in ev:
        return CloseProjectEvent()
    elif "RemoveProjectEvent" in ev:
        return RemoveProjectEvent()
    elif "GenInviteEvent" in ev:
        return GenInviteEvent()
    elif "JoinProjectEvent" in ev:
        return JoinProjectEvent()
    elif "LeaveProjectEvent" in ev:
        return LeaveProjectEvent()
    elif "CreateRoleEvent" in ev:
        return CreateRoleEvent(**ev["CreateRoleEvent"])
    elif "UpdateRoleEvent" in ev:
        return UpdateRoleEvent(**ev["UpdateRoleEvent"])
    elif "RemoveRoleEvent" in ev:
        return RemoveRoleEvent(**ev["RemoveRoleEvent"])
    elif "UpdateProjectMemberEvent" in ev:
        return UpdateProjectMemberEvent(**ev["UpdateProjectMemberEvent"])
    elif "RemoveProjectMemberEvent" in ev:
        return RemoveProjectMemberEvent(**ev["RemoveProjectMemberEvent"])
    elif "SetProjectMemberRoleEvent" in ev:
        return SetProjectMemberRoleEvent(**ev["SetProjectMemberRoleEvent"])
    elif "UploadWorkSnapShotEvent" in ev:
        return UploadWorkSnapShotEvent(**ev["UploadWorkSnapShotEvent"])
    elif "CreateChannelEvent" in ev:
        return CreateChannelEvent(**ev["CreateChannelEvent"])
    elif "UpdateChannelEvent" in ev:
        return UpdateChannelEvent(**ev["UpdateChannelEvent"])
    elif "OpenChannelEvent" in ev:
        return OpenChannelEvent(**ev["OpenChannelEvent"])
    elif "CloseChannelEvent" in ev:
        return CloseChannelEvent(**ev["CloseChannelEvent"])
    elif "RemoveChannelEvent" in ev:
        return RemoveChannelEvent(**ev["RemoveChannelEvent"])
    elif "AddChannelMemberEvent" in ev:
        return AddChannelMemberEvent(**ev["AddChannelMemberEvent"])
    elif "RemoveChannelMemberEvent" in ev:
        return RemoveChannelMemberEvent(**ev["RemoveChannelMemberEvent"])
    elif "CreateAppraiseEvent" in ev:
        return CreateAppraiseEvent(**ev["CreateAppraiseEvent"])
    elif "AddProjectAppEvent" in ev:
        return AddProjectAppEvent(**ev["AddProjectAppEvent"])
    elif "RemoveProjectAppEvent" in ev:
        return RemoveProjectAppEvent(**ev["RemoveProjectAppEvent"])
    else:
        return None
