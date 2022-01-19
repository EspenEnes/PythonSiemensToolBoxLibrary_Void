from dataclasses import dataclass , InitVar
from projectFiles import Step7ProjectV5


@dataclass()
class ProjectFolder():
    Name = None
    Author = None
    Comment = None
    Created = None
    Modified = None

    # project = project
    parent : InitVar[Step7ProjectV5] = None

    subItems = []

    def __post_init__(self, parent):
        self.Name = parent.projectName
        self.parent = parent

    def __repr__(self):
        return f"{self.parent}"

