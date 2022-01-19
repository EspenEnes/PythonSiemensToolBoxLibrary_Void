from DBF.parseDBF import ParseDBF
from .getLayout import Getlayout
from .getTimeStamp import GetTimeStamp
from datatypes import BlockType as PLCBlockType
from datatypes import S7ProjectBlockInfo, BlockBytes


class BlockOfflineFolder():
    def __init__(self):
        self._loaded = False
        self.name = None
        self.folder = None
        self.ID = None
        self.parent = None
        self.blockList = {}
        self._retrevedblockbytes = dict()
        self._retrevedblockLayout = dict()

    def initReadPlcBlocklist(self):
        bausteinDBF = ParseDBF(f"{self.folder}\\BAUSTEIN.DBF")
        subblkDBF = ParseDBF(f"{self.folder}\\SUBBLK.DBF")
        blocks = {}
        retval = {}

        if not bausteinDBF or not subblkDBF:
            return blocks

        for row in bausteinDBF.records:
            if int(row["TYP"]) in [PLCBlockType.SFB.value, PLCBlockType.SFC.value, PLCBlockType.SDB.value,
                                   PLCBlockType.DB.value,
                                   PLCBlockType.VAT.value, PLCBlockType.FB.value, PLCBlockType.FC.value,
                                   PLCBlockType.OB.value,
                                   PLCBlockType.UDT.value]:
                tmp = S7ProjectBlockInfo()
                # tmp.ParentFolder = self
                tmp.parent = self
                tmp.Deleted = False
                tmp.BlockNumber = int(row["NUMMER"])
                tmp.id = int(row["ID"])
                tmp.BlockType = PLCBlockType(int(row["TYP"]))
                blocks[str(tmp.id)] = tmp

        typ = [PLCBlockType.FC.value, PLCBlockType.OB.value, PLCBlockType.FB.value, PLCBlockType.SFC.value]

        for row in subblkDBF.records:
            id = int(row["OBJECTID"])
            try:
                block = blocks[str(id)]
                if int(row["SUBBLKTYP"]) in typ:
                    block.Name = row["BLOCKNAME"]
                    block.Family = row["BLOCKFNAME"]
                    if int(row["SUBBLKTYP"]) != PLCBlockType.SFC.value:
                        if int(row["PASSWORD"]) == 3:
                            block.KnowHowProtection = True
            except KeyError:
                continue

            retval[block.BlockName] = block

            # if block.id == int(row["OBJECTID"]) and int(row["SUBBLKTYP"]) in typ:
            #     block.Name = row["BLOCKNAME"]
            #     block.Family = row["BLOCKFNAME"]
            #     if int(row["SUBBLKTYP"]) != PLCBlockType.SFC.value:
            #         if int(row["PASSWORD"]) == 3:
            #             block.KnowHowProtection = True
        return retval

    def load(self):
        self._loaded = True
        if not len(self.blockList) > 0:
            self.blockList = self.initReadPlcBlocklist()
        return list(self.blockList.keys())

    def GetBlockBytes(self, blkinfo):

        if not blkinfo:
            return None

        if str(blkinfo.id) in self._retrevedblockbytes:
            return self._retrevedblockbytes[str(blkinfo.id)]

        if not hasattr(self, "bausteinDBF"):
            self.bausteinDBF = ParseDBF(f"{self.folder}\\BAUSTEIN.DBF", encoding="ISO-8859-1")
        if not hasattr(self, "subblkDBF"):
            self.subblkDBF = ParseDBF(f"{self.folder}\\SUBBLK.DBF", encoding="ISO-8859-1")

        blockbytes = BlockBytes()

        for row in self.bausteinDBF.records:
            if not int(row["ID"]) == blkinfo.id:
                continue
            if row["UDA"]:
                blockbytes.uda = row["UDA"]

        for row in self.subblkDBF.records:
            if not int(row["OBJECTID"]) == blkinfo.id:
                continue

            mc5code = None
            if row["MC5CODE"] is not None:
                mc5code = row["MC5CODE"]
                if len(mc5code) > int(row["MC5LEN"]):
                    mc5code = mc5code.zfill(int(row["MC5LEN"]))

            ssbpart = None
            if row["SSBPART"] is not None:
                ssbpart = row["SSBPART"]
                if len(ssbpart) > int(row["SSBLEN"]):
                    ssbpart = ssbpart.zfill(int(row["SSBLEN"]))

            addinfo = None
            if row["ADDINFO"] is not None:
                addinfo = row["ADDINFO"]
                if len(addinfo) > int(row["ADDLEN"]):
                    addinfo = addinfo.zfill(int(row["ADDLEN"]))

            if blockbytes.CheckSum == 0:
                if int(row["CHECKSUM"] != 0):
                    blockbytes.CheckSum = int(row["CHECKSUM"])

            if row["SUBBLKTYP"] in [
                PLCBlockType.SDB.value, PLCBlockType.OB.value, PLCBlockType.FB.value, PLCBlockType.SFC.value,
                PLCBlockType.SFB.value]:

                if int(row["PASSWORD"]) == 3:
                    blockbytes.knowHowProtection = True

                blockbytes.mc7code = mc5code
                blockbytes.username = str(row["USERNAME"]).strip("\0")
                blockbytes.version = str(int(row["VERSION"]) / 16) + "." + str(int(row["VERSION"]) % 16)
                blockbytes.nwinfo = addinfo
                blockbytes.LastCodeChange = GetTimeStamp(row["TIMESTAMP1"])
                blockbytes.LastInterfaceChange = GetTimeStamp(row["TIMESTAMP2"])
                # blockbytes.BlockLanguage = PLCLanguage(int(row["BLKLANG"]))


            elif int(row["SUBBLKTYP"]) in [5, 3, 4, 7, 9]:
                if mc5code is not None:
                    blockbytes.blkinterface = str(mc5code)

            elif int(row["SUBBLKTYP"]) in [19, 17, 18, 22, 21]:
                blockbytes.comments = mc5code
                blockbytes.blockdescription = ssbpart
                blockbytes.jumpmarks = addinfo

            elif int(row["SUBBLKTYP"]) in [1, 6]:
                if mc5code is not None:
                    blockbytes.blkinterface = str(mc5code)
                blockbytes.addinfo = addinfo

                blockbytes.LastCodeChange = GetTimeStamp(row["TIMESTAMP1"])
                blockbytes.LastInterfaceChange = GetTimeStamp(row["TIMESTAMP2"])

            elif int(row["SUBBLKTYP"]) == 10:
                blockbytes.mc7code = mc5code
                blockbytes.blkinterfaceInMC5 = ssbpart
                blockbytes.LastCodeChange = GetTimeStamp(row["TIMESTAMP1"])
                blockbytes.LastInterfaceChange = GetTimeStamp(row["TIMESTAMP2"])

                bytearrayOfssbpart = bytearray(ssbpart, encoding="ISO-8859-1")
                if int(row["SSBLEN"]) > 2 and (bytearrayOfssbpart[0] == 0x0a or bytearrayOfssbpart[0] == 0x0b):
                    blockbytes.IsInstanceDB = True
                    if bytearrayOfssbpart[0] == 11:
                        blockbytes.IsSFB = True
                    try:
                        blockbytes.FBNumber = int(bytearrayOfssbpart[1] + (256 * int(bytearrayOfssbpart[2])))
                    except IndexError:
                        print(blkinfo)

            elif int(row["SUBBLKTYP"]) == 14:
                pass

            elif int(row["SUBBLKTYP"]) == 42:
                pass

            elif int(row["SUBBLKTYP"]) == 27:  # VAT
                blockbytes.LastCodeChange = GetTimeStamp(row["TIMESTAMP1"])
                blockbytes.LastInterfaceChange = GetTimeStamp(row["TIMESTAMP2"])
                blockbytes.mc7code = mc5code
                blockbytes.nwinfo = addinfo

            elif int(row["SUBBLKTYP"]) == 38:
                blockbytes.comments = mc5code
        self._retrevedblockbytes[str(blkinfo.id)] = blockbytes

        return blockbytes

    def GetBlock(self, BlockName=None, blkInfo=None):
        if not self._loaded:
            self.load()

        if BlockName:
            blkInfo = self.GetProjectBlockInfoFromBlockName(BlockName)
            return self.GetBlockBytes(blkInfo)
        elif blkInfo:
            return self.GetBlockBytes(blkInfo)
        return None

    def GetProjectBlockInfoFromBlockName(self, BlockName: str) -> S7ProjectBlockInfo or None:
        if len(self.blockList) < 1:
            self.blockList = self.initReadPlcBlocklist()

        try:
            return self.blockList[BlockName.upper()]
        except KeyError:
            return None

    def getLayout(self, blockName=None, blkInfo=None):
        if blockName:
            blkinfo = self.GetProjectBlockInfoFromBlockName(blockName)
        else:
            blkinfo = blkInfo

        if str(blkinfo.id) in self._retrevedblockLayout:
            return self._retrevedblockLayout[str(blkinfo.id)]

        blkbytes = self.GetBlockBytes(blkinfo)
        if not blkbytes.blkinterface:
            return Getlayout(self, [])
        rows = [row.strip() for row in blkbytes.blkinterface.split("\n") if len(row.strip()) > 0]
        root = Getlayout(self, rows)
        self._retrevedblockLayout[str(blkinfo.id)] = root
        return root

    def __str__(self):
        return self.name.decode("ISO-8859-1")

    def __iter__(self):

        for block in self.blockList.values():
            yield block

    # def __repr__(self):
    #     return str(self.blockList.keys())

    def __getitem__(self, item) -> S7ProjectBlockInfo or None:
        if not self._loaded:
            self.load()

        if isinstance(item, str):
            try:
                return self.blockList[item.upper()]
            except KeyError:
                return None
        if isinstance(item, int):
            try:
                name = list(self.blockList)[item]

                return self.blockList[name]
            except LookupError:
                return None
