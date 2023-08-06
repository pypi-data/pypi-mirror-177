from typing import Mapping, Any


class AddRepoEvent:  # 创建仓库
    def __init__(self, repo_id: str = "", repo_url: str = "", **params):
        self.repo_id = repo_id
        self.repo_url = repo_url


class RemoveRepoEvent:  # 删除仓库
    def __init__(self, repo_id: str = "", repo_url: str = "", **params):
        self.repo_id = repo_id
        self.repo_url = repo_url


class CreateActionEvent:  # 创建执行命令
    def __init__(self, repo_id: str = "", repo_url: str = "", action_id: str = "", action_name: str = "", **params):
        self.repo_id = repo_id
        self.repo_url = repo_url
        self.action_id = action_id
        self.action_name = action_name


class UpdateActionEvent:  # 更新执行命令
    def __init__(self, repo_id: str, repo_url: str = "", action_id: str = "", action_name: str = "", **params):
        self.repo_id = repo_id
        self.repo_url = repo_url
        self.action_id = action_id
        self.action_name = action_name


class RemoveActionEvent:  # 删除执行命令
    def __init__(self, repo_id: str = "", repo_url: str = "", action_id: str = "", action_name: str = "", **params):
        self.repo_id = repo_id
        self.repo_url = repo_url
        self.action_id = action_id
        self.action_name = action_name


EarthlyEvents = AddRepoEvent | RemoveRepoEvent | CreateActionEvent | UpdateActionEvent | RemoveActionEvent | None


def parseEarthlyEvent(ev: Mapping[str, Mapping[str, Any]]) -> EarthlyEvents:
    if "AddRepoEvent" in ev:
        return AddRepoEvent(**ev["AddRepoEvent"])
    elif "RemoveRepoEvent" in ev:
        return RemoveRepoEvent(**ev["RemoveRepoEvent"])
    elif "CreateActionEvent" in ev:
        return CreateActionEvent(**ev["CreateActionEvent"])
    elif "UpdateActionEvent" in ev:
        return UpdateActionEvent(**ev["UpdateActionEvent"])
    elif "RemoveActionEvent" in ev:
        return RemoveActionEvent(**ev["RemoveActionEvent"])
    else:
        return None
