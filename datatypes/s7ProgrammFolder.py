from dataclasses import dataclass

@dataclass
class S7ProgrammFolder:
    Name = None
    parent = None
    _linkfileoffset = None
    blockOfflineFolder = None
    symbolTable = None
    # self.onlineBlocksFolder = None
    # self.sourceFolder = None
    ID = None

    @property
    def blocks(self):
        return self.blockOfflineFolder.blockList

    def __str__(self):
        return self.Name

    def __repr__(self):
        return self.Name

    def load(self):
        self.symbolTable.load()
        list = self.blockOfflineFolder.load()
        return list
