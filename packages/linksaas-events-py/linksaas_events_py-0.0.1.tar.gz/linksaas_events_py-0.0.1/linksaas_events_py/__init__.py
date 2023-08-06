from typing import Mapping, Any

from .project_book_shelf_events import parseBookShelfEvent, BookShelfEvents
from .project_doc_events import parseDocEvent, DocEvents
from .project_earthly_events import parseEarthlyEvent, EarthlyEvents
from .project_events import parseProjectEvent, ProjectEvents
from .project_ext_event_events import parseExtEvent, ExtEvents
from .project_gitee_events import parseGiteeEvent, GiteeEvents
from .project_gitlab_events import parseGitlabEvent, GitlabEvents
from .project_issue_event import parseIssueEvent, IssueEvents
from .project_robot_events import parseRobotEvent, RobotEvents
from .project_sprit_events import parseSpritEvent, SpritEvents


AllEvents = BookShelfEvents | DocEvents | EarthlyEvents | ProjectEvents | ExtEvents | GiteeEvents | GitlabEvents | IssueEvents | RobotEvents | SpritEvents | None


def parseAllEvent(ev: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> AllEvents:
    if "ProjectEvent" in ev:
        return parseProjectEvent(ev["ProjectEvent"])
    elif "ProjectDocEvent" in ev:
        return parseDocEvent(ev["ProjectDocEvent"])
    elif "SpritEvent" in ev:
        return parseSpritEvent(ev["SpritEvent"])
    elif "IssueEvent" in ev:
        return parseIssueEvent(ev["IssueEvent"])
    elif "BookShelfEvent" in ev:
        return parseBookShelfEvent(ev["BookShelfEvent"])
    elif "ExtEvEvent" in ev:
        return parseExtEvent(ev["ExtEvEvent"])
    elif "GitlabEvent" in ev:
        return parseGitlabEvent(ev["GitlabEvent"])
    elif "GiteeEvent" in ev:
        return parseGiteeEvent(ev["GiteeEvent"])
    elif "RobotEvent" in ev:
        return parseRobotEvent(ev["RobotEvent"])
    elif "EarthlyEvent" in ev:
        return parseEarthlyEvent(ev["EarthlyEvent"])
    else:
        return None
