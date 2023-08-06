from typing import Mapping, Any


class PushEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class IssueEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class PullRequestEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class NoteEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


GiteeEvents = PushEvent | IssueEvent | PullRequestEvent | NoteEvent | None


def parseGiteeEvent(ev: Mapping[str, Mapping[str, Any]]) -> GiteeEvents:
    if "PushEvent" in ev:
        return PushEvent(**ev["PushEvent"])
    elif "IssueEvent" in ev:
        return IssueEvent(**ev["IssueEvent"])
    elif "PullRequestEvent" in ev:
        return PullRequestEvent(**ev["PullRequestEvent"])
    elif "NoteEvent" in ev:
        return NoteEvent(**ev["NoteEvent"])
    else:
        return None
