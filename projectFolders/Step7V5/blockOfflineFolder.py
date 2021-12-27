from DBF.parseDBF import ParseDBF
from SimaticTools.datatypes import PLCBlockType
from SimaticTools.blocks import S7ProjectBlockInfo
from collections import OrderedDict

class BlockOfflineFolder():
    def __init__(self):
        self.name = None
        self.folder = None
        self.ID = None

    def initReadPlcBlocklist(self):
        bausteinDBF = ParseDBF(f"{self.folder}\\BAUSTEIN.DBF")
        subblkDBF = ParseDBF(f"{self.folder}\\SUBBLK.DBF")
        blocks = []

        if not bausteinDBF or not subblkDBF:
            return blocks

        for row in bausteinDBF.getColumns(["TYP", "NUMMER", "ID"], "ISO-8859-1"):
            if int(row["TYP"]) in [PLCBlockType.SFB.value, PLCBlockType.SFC.value, PLCBlockType.SDB.value, PLCBlockType.DB.value,
                       PLCBlockType.VAT.value, PLCBlockType.FB.value, PLCBlockType.FC.value, PLCBlockType.OB.value,
                       PLCBlockType.UDT.value]:

                tmp = S7ProjectBlockInfo()
                tmp.ParentFolder = self
                tmp.Deleted = False
                tmp.BlockNumber = int(row["NUMMER"])
                tmp.id = int(row["ID"])
                tmp.BlockType = PLCBlockType(int(row["TYP"]))
                blocks.append(tmp)

        typ = [PLCBlockType.FC.value, PLCBlockType.OB.value, PLCBlockType.FB.value, PLCBlockType.SFC.value]

        for block in blocks:
            for row in subblkDBF.records:
                if block.id == int(row["OBJECTID"]) and int(row["SUBBLKTYP"]) in typ:
                    block.Name = row["BLOCKNAME"]
                    block.Family = row["BLOCKFNAME"]
                    if int(row["SUBBLKTYP"]) != PLCBlockType.SFC.value:
                        if int(row["PASSWORD"]) == 3:
                            block.KnowHowProtection = True
        return blocks


    def readPlcBlockList(self):
        return self.initReadPlcBlocklist()

    def GetBlock(self, BlockName=None, blkInfo=None):
        pass