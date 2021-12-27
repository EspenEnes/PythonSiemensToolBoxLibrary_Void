from dataclasses import dataclass, field, _MISSING_TYPE

from SimaticTools.datatypes import PLCBlockType


@dataclass
class IProjectBlockInfo:
    Name: str = field(default_factory=_MISSING_TYPE)
    ParentFolder: str = field(default_factory=_MISSING_TYPE)
    BlockType: PLCBlockType = field(default_factory=_MISSING_TYPE)

@dataclass
class ProjectBlockInfo(IProjectBlockInfo):
    id: int = field(default_factory=_MISSING_TYPE)
    _Block = None
    IsInstance: bool = False

    Deleted: bool = field(default_factory=_MISSING_TYPE)

    def ToString(self):
        if not self.Deleted:
            return self.Name
        return f"{self.Name}$$_"

    def GetBlock(self):
        pass

    def GetSourceBlock(self):
        pass

    def BlockTypeString(self):

        if self.BlockType == PLCBlockType.DB:
            return "Datablock"
        elif self.BlockType == PLCBlockType.FB:
            return "Functionblock"
        elif self.BlockType == PLCBlockType.FC:
            return "Function"
        elif self.BlockType == PLCBlockType.OB:
            return "Organisationblock"
        elif self.BlockType == PLCBlockType.UDT:
            return "Userdatatype"
        elif self.BlockType == PLCBlockType.VAT:
            return "Variabletable"
        elif self.BlockType == PLCBlockType.SFC:
            return "Systemfunction"
        elif self.BlockType.S5_DB:
            return "S5-Datablock"
        elif self.BlockType.S5_FB:
            return "S5-Functionblock"
        elif self.BlockType.S5_PB:
            return "S5-Programblock"
        elif self.BlockType.S5_FX:
            return "S5-ExtenedFunctionblock"
        elif self.BlockType.S5_SB:
            return "S5-Stepblock"
        elif self.BlockType.S5_DV:
            return "S5-Datablock-Preheader"
        elif self.BlockType.S5_FV:
            return "S5-Functionblock-Preheader"
        elif self.BlockType.S5_FVX:
            return "S5-Extendedfunctionblock-Preheader"
        elif self.BlockType.S5_DX:
            return "S5-Extendeddatablock"
        elif self.BlockType.S5_DVX:
            return "S5-Extendeddatablock-Preheader"
        elif self.BlockType.S5_OB:
            return "S5-Organisationblock"
        elif self.BlockType.S5_PK:
            return "S5-Programcommentblock"
        elif self.BlockType.S5_FK:
            return "S5-Functioncommentblock"
        elif self.BlockType.S5_FKX:
            return "S5-Extendedfunctioncommentblock"
        elif self.BlockType.S5_SK:
            return "S5-Stepcommentblock"
        elif self.BlockType.S5_DK:
            return "S5-Datacommentblock"
        elif self.BlockType.S5_DKX:
            return "S5-Extendeddatacommentblock"
        elif self.BlockType.S5_OK:
            return "S5-Organisationcommentblock"
        elif self.BlockType.S5_BB:
            return "S5-Variabletable"
        elif self.BlockType == PLCBlockType.SourceBlock:
            return "Sourceblock"
        return ""

    def Export(self):
        pass

    def BlockLanguage(self):
        pass



@dataclass
class ProjectPlcBlockInfo(ProjectBlockInfo):
    SymbolTableEntry = None
    BlockNumber: int = field(default_factory=_MISSING_TYPE)

    @property
    def BlockName(self):
        if not self.Deleted:
            return f"{self.BlockType.name}{self.BlockNumber}"
        return f"$$_{self.BlockType.name}{self.BlockNumber}"

    def ToString(self):
        if not self.Deleted and self.SymbolTableEntry is not None:
            return self.BlockName
        retval = ""
        if self.Deleted:
            retval += "$$_"
        if self.SymbolTableEntry is not None:
            retval += self.BlockName + " (SymbolTabelEntry.Symbol)" #todo sjekk
        return retval

#
@dataclass
class S7ProjectBlockInfo(ProjectPlcBlockInfo):
    @property
    def Family(self):
        return self._Family

    @Family.setter
    def Family(self, value):
        self._Family = value


    @property
    def KnowHowProtection(self):
        return self._KnowHowProtection

    @KnowHowProtection.setter
    def KnowHowProtection(self, value: bool):
        self._KnowHowProtection = value

    def ToString(self):
        if not self.KnowHowProtection:
            return ProjectPlcBlockInfo.ToString(self)
        return f"@{ProjectPlcBlockInfo.ToString(self)}"
#








