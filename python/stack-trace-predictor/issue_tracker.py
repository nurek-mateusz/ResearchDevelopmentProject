from jira import JIRA
from print_function_helpers import dprint


def fetch_range(jira_url: str, issue_id: str) -> (str, str):
    jira = JIRA(jira_url)

    issue = jira.issue(issue_id)

    if issue is None:
        raise SystemExit(
            "Couldn't retireve issue from the server. Is issue id and url ok?")

    dprint(issue.id)
    dprint(issue.fields.created)

    return (None, issue.fields.created)
