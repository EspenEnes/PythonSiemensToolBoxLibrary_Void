import os.path
import re
from DBF import ParseDBF
from .Project import Project
from projectFolders import getProjectfolder, getProjectEncoding, ProjectFolder
from datatypes import PLCType

from projectFolders.Step7V5 import getAllBlocksOfflineFolders, getAllProgramFolders, symbolTable, getAllProjectStations, \
    getAllCpuFolders, getAllNetworkInterfaces, getAllDP, getAllMPI, getAllCommunicationProcessors




class Step7ProjectV5(Project):
    def __init__(self, projectfile):
        super(Step7ProjectV5, self).__init__()
        self.projectFolder, self.projectFile, self.ziphelper = getProjectfolder(projectfile)
        self.projectEncoding = getProjectEncoding(self)
        self._cpuFolders = {}
        self._s7ProgrammFolders = {}

        self.loadProjectHeader()

    def loadProjectHeader(self) -> str: #todo read Projectheader without unpacking zipfile
        with open(self.projectFile, "rb") as f:
            data = f.read()
            startindex = 5
            span = int(data[startindex - 1])
            stopindex = startindex + span
            self.projectName = data[startindex: stopindex].decode("ISO-8859-1")

            startindex = stopindex + 5
            span = int(data[startindex - 1])
            stopindex = startindex + span
            projectDescription = data[startindex: stopindex]
        return f"{self.projectName}"

    def load(self) -> list:
        self.projectStructure = ProjectFolder(self)

        #Get project Stations
        self._stations = getAllProjectStations(self)

        #Get project CPUs and link to Stations
        self._cpuFolders = getAllCpuFolders(self)
        self._cpFolders = getAllCommunicationProcessors(self)

        #Get project NetworkInterfaces todo: Link interface with CPU
        self._networkInterfaces = getAllNetworkInterfaces(self)
        self.MPI = getAllMPI(self)
        self.DP = getAllDP(self)


        self._s7ProgrammFolders = getAllProgramFolders(self)
        self._blocksOfflineFolders = getAllBlocksOfflineFolders(self)

        self._linkProgrammFolderWithCPU()
        self._linkOfflineblockFolderWithProgrammFolder()
        self._linkSymbolTableWithProgrammFolder()
        self._linkProfinetWithCpuCp()

        self._loaded = True

        return [folder for folder in self._s7ProgrammFolders.values()]


    def _linkProgrammFolderWithCPU(self):
        dbf = ParseDBF(fr"{self.projectFolder}\hOmSave7\s7hk31ax\HRELATI1.DBF")
        for row in dbf.records:
            if int(row["RELID"]) == 16:
                cpuID = int(row["SOBJID"])
                folderID = int(row["TOBJID"])

                if cpuID in self._cpuFolders.keys() and folderID in self._s7ProgrammFolders:
                    cpu = self._cpuFolders[cpuID]
                    folder = self._s7ProgrammFolders[folderID]
                    folder.parent = cpu
                    cpu.subItems.append(folder)

    def _linkOfflineblockFolderWithProgrammFolder(self):
        file = self.projectFolder + "\\" + "hrs" + "\\" + "linkhrs.lnk"
        with open(file, "rb") as f:
            completeBuffer = f.read()

        for S7ProgrammFolder in self._s7ProgrammFolders.values():
            position = S7ProgrammFolder._linkfileoffset

            match = re.compile(b"\x01\x60\x11\x00(.{2})").search(completeBuffer[position:])
            if match:
                Step7ProjectBlockFolderID = int.from_bytes(match.group(1), "little")

                for blocksOfflineFolders in self._blocksOfflineFolders:
                    if Step7ProjectBlockFolderID == int(blocksOfflineFolders.ID):
                        S7ProgrammFolder.blockOfflineFolder = blocksOfflineFolders
                        blocksOfflineFolders.parent = S7ProgrammFolder
                        break

    def _linkSymbolTableWithProgrammFolder(self):
        dbf1 = ParseDBF(f"{self.projectFolder}\\YDBs\\YLNKLIST.DBF")
        dbf2 = ParseDBF(f"{self.projectFolder}\\YDBs\\SYMLISTS.DBF")

        id2 = 0
        for folder in self._s7ProgrammFolders.values():
            for row in dbf1.records:
                if int(row["TOI"]) == folder.ID:
                    id2 = int(row["SOI"])
                    break

            if id2 > 0:
                for row in dbf2.records:
                    if not int(row["_ID"]) == id2:
                        continue

                    if os.path.isfile(f"{self.projectFolder}\\YDBs\\{str(id2)}\\SYMLIST.DBF"):
                        table = symbolTable.SymbolTable()
                        table.Name = (row["_UNAME"])
                        table.folder = f"{self.projectFolder}\\YDBs\\{str(id2)}"
                        folder.symbolTable = table
                        break

    def _linkProfinetWithCpuCp(self):
        plcsWithEternet = [PLCType.EternetInCPU3xxF.value, PLCType.EternetInCPU3xx.value, PLCType.EternetInCPU4xx.value,
                           PLCType.EternetInCPU3xx_2.value, PLCType.EternetInCPURTX.value]

        dbf = ParseDBF(
            fr"{self.projectFolder}\hOmSave7\s7hssiox\HOBJECT1.DBF")

        for row in dbf.records:
            if int(row["OBJTYP"]) in plcsWithEternet:
                """Profinet connection to CPU"""
                if int(row["UNITID"]) in self.cpuFolders:
                    cpu = self.cpuFolders[int(row["UNITID"])]
                    cpu.idTobjID.append(int(row["ID"]))
            elif int(row["OBJTYP"]) in [2364971, 2367589]:
                if int(row["UNITID"]) in self.cpFolders:
                    cp = self.cpFolders[int(row["UNITID"])]
                    cp.idTobjId.append(int[row["ID"]])

        dbf = ParseDBF(fr"{self.projectFolder}\hOmSave7\s7hssiox\HRELATI1.DBF")
        for row in dbf.records:
            if int(row["RELID"]) == 64:
                CP = next((cp for cp in self.cpFolders.values() if int(row["SOBJID"]) in cp.idTobjId), None)
                CPU = next((cpu for cpu in self.cpuFolders.values() if int(row["SOBJID"]) in cpu.idTobjID), None)
                if CP:
                    CP.tObjId = int(row["TOBJID"])  #todo: this is alo done in getAll_CP  ????
                elif CPU:
                    CPU.tObjId = int(row["TOBJID"])

        for networkId in self._networkInterfaces:
            CPU = next((cpu for cpu in self.cpuFolders.values() if cpu.tObjId == networkId), None)
            CP = next((cp for cp in self.cpFolders.values() if networkId == cp.tObjId), None)
            if CP:
                CP.NetworkInterfaces.append(self._networkInterfaces[networkId])
            if CPU:
                CPU.NetworkInterfaces.append(self._networkInterfaces[networkId])
    @property
    def station(self):
        return self._stations

    @property
    def cpuFolders(self):
        return self._cpuFolders

    @property
    def cpFolders(self):
        return self._cpFolders

    @property
    def s7ProgrammFolders(self):
        return self._s7ProgrammFolders

    # @property
    # def blockOfflineFolders(self):
    #     if not self._loaded:
    #         self.load()
    #     return self._blocksOfflineFolders
