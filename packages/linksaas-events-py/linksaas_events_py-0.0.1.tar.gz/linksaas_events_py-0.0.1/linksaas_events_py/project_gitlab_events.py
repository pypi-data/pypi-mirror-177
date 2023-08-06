from typing import Mapping, Any

class BuildEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class CommentEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class IssueEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class JobEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class MergeRequestEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class PipelineEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class PushEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class TagEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v


class WikiEvent:
    def __init__(self, **param):
        for k, v in param.items():
            self.__dict__[k] = v

GitlabEvents = BuildEvent|CommentEvent|IssueEvent|JobEvent|MergeRequestEvent|PipelineEvent|PushEvent|TagEvent|WikiEvent|None

def parseGitlabEvent(ev: Mapping[str, Mapping[str, Any]]) -> GitlabEvents:
    if "BuildEvent" in ev:
        return BuildEvent(**ev["BuildEvent"])
    elif "CommentEvent" in ev:
        return CommentEvent(**ev["CommentEvent"])
    elif "IssueEvent" in ev:
        return IssueEvent(**ev["IssueEvent"])
    elif "JobEvent" in ev:
        return JobEvent(**ev["JobEvent"])
    elif "MergeRequestEvent" in ev:
        return MergeRequestEvent(**ev["MergeRequestEvent"])
    elif "PipelineEvent" in ev:
        return PipelineEvent(**ev["PipelineEvent"])
    elif "PushEvent" in ev:
        return PushEvent(**ev["PushEvent"])
    elif "TagEvent" in ev:
        return TagEvent(**ev["TagEvent"])
    elif "WikiEvent" in ev:
        return WikiEvent(**ev["WikiEvent"])
    else:
        return None
