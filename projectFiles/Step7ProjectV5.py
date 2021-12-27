from .Project import Project
from SimaticTools import getProjectfolder, getProjectEncoding
from projectFolders.Step7V5 import getAllBlocksOfflineFolders, getAllProgramFolders
import re


class Step7ProjectV5(Project):
    def __init__(self, projectfile, showDeleted=False):
        super(Step7ProjectV5, self).__init__()
        self.projectFolder, self.projectFile, self.ziphelper = getProjectfolder(projectfile)

        self.projectEncoding = getProjectEncoding(self.projectFolder)
        self._showDeleted = showDeleted
        self._blocksOfflineFolders = list()
        self.loadProjectHeader(self._showDeleted)


    def loadProjectHeader(self, showDeleted):
        self._showDeleted = showDeleted
        with open( self.projectFile, "rb") as f:
            data = f.read()
            startindex = 5
            span = int(data[startindex - 1])
            stopindex = startindex + span
            self.projectName = data[startindex: stopindex].decode("ISO-8859-1")

            startindex = stopindex + 5
            span = int(data[startindex - 1])
            stopindex = startindex + span
            self.projectDescription = data[startindex: stopindex]

    def loadProject(self):
        self.projectStructure = None
        self.s7ProgrammFolders = getAllProgramFolders(self.projectFolder)
        self._blocksOfflineFolders = getAllBlocksOfflineFolders(self.projectFolder, self.projectEncoding[0])
        self.linkOfflineblockFolderWithProgrammFolder()

    def linkOfflineblockFolderWithProgrammFolder(self):
        file = self.projectFolder + "\\" + "hrs" + "\\" + "linkhrs.lnk"
        with open(file, "rb") as f:
            completeBuffer = f.read()

        for S7ProgrammFolder in self.s7ProgrammFolders:
            position = S7ProgrammFolder._linkfileoffset

            match = re.compile(b"\x01\x60\x11\x00(.{2})").search(completeBuffer[position:])
            if match:
                Step7ProjectBlockFolderID = int.from_bytes(match.group(1), "little")

                for blocksOfflineFolders in self._blocksOfflineFolders:
                    if Step7ProjectBlockFolderID == int(blocksOfflineFolders.ID):
                        S7ProgrammFolder.blockOfflineFolder = blocksOfflineFolders
                        break








