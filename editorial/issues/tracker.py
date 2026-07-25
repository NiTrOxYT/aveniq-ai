"""
Structured Issue Tracker for Editorial Department.
Converts all reviewer findings into structured EditorialIssue objects.
"""

from typing import List, Dict, Any
from editorial.models.schema import EditorialIssue

class IssueTracker:
    def __init__(self):
        self.issues: List[EditorialIssue] = []

    def add_issue(
        self,
        severity: str,
        category: str,
        location: str,
        description: str,
        suggested_fix: str,
        reviewer: str
    ) -> EditorialIssue:
        issue_id = f"iss_{category.lower()[:3]}_{len(self.issues) + 1:03d}"
        issue = EditorialIssue(
            id=issue_id,
            severity=severity,
            category=category,
            location=location,
            description=description,
            suggested_fix=suggested_fix,
            status="Open",
            reviewer=reviewer
        )
        self.issues.append(issue)
        return issue

    def get_blocking_issues(self) -> List[EditorialIssue]:
        return [i for i in self.issues if i.severity in ["Critical", "High"] and i.status == "Open"]
