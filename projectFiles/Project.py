


class Project():
    def __init__(self):
        self.projectFile = None
        self.projectFolder = None
        self.projectName = None
        # self.projectDescription = None
        self.projectEncoding = None
        self._allFolders = []
        self._loaded = False

    def __str__(self):
        if self.projectName:
            return self.projectName
        return self.projectFile

    def __repr__(self):
        if self.projectName:
            return self.projectName
        return self.projectFile




