from dataclasses import dataclass


@dataclass
class BlockBytes:
    mc7code: bytes = None
    uda: bytes = None
    subblocks: bytes = None
    comments: bytes = None
    addinfo: bytes = None
    blkinterface: str = None
    blkinterfaceInMC5: bytes = None
    nwinfo: bytes = None
    blockdescription: bytes = None
    jumpmarks: bytes = None
    knowHowProtection: bool = False
    username: str = None
    version: str = None
    LastCodeChange = None
    LastInterfaceChange = None
    IsInstanceDB: bool = False
    IsSFB: bool = False
    FBNumber: int = None
    CheckSum: int = 0

    BlockLanguage = None
