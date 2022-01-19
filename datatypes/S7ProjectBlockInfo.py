from dataclasses import dataclass
from .BlockType import BlockType, BlockTypeString


@dataclass
class S7ProjectBlockInfo():
    family: str = None
    knowHowProtection: bool = False
    BlockNumber: int = None
    id: int = None
    parent = None
    name = None
    BlockType : BlockType = None
    isInstance = False
    Deleted: bool = False # Not used

    _block = None


    def load(self): #GetBlock
        if not self._block:
            self._block = self.parent.GetBlock(blkInfo=self)
        return self._block

    @property
    def symbol(self):
        symbol =  self.parent.parent.symbolTable[self.BlockName]
        if symbol:
            return symbol.decode('ISO-8859-1').strip()
        return symbol

    @property
    def BlockName(self):
        return f"{self.BlockType.name}{self.BlockNumber}"

    @property
    def BlockTypeSting(self):
        return BlockTypeString(self.BlockType)

    @property
    def layout(self):
        layout =  self.parent.getLayout(blkInfo=self)
        return layout.dbLayout


    def __str__(self):
        retval = ""
        if self.knowHowProtection:
            retval = "@"
        if self.symbol:
            return f"{retval}{self.BlockName} ({self.symbol})"
        return f"{retval}{self.BlockName}"

    def __repr__(self):
        retval = ""
        if self.knowHowProtection:
            retval = "@"
        if self.symbol:
            return f"{retval}{self.BlockName} ({self.symbol})"
        return f"{retval}{self.BlockName}"


if __name__ == '__main__':
    block = S7ProjectBlockInfo()