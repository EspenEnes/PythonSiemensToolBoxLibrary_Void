from dataclasses import dataclass


@dataclass
class CpFolder:
    ID = None
    parent = None
    name = None
    unitID: int = None
    objTyp: int = None
    tObjTyp: int = None
    subModulNumber: int = None

    rack: int = None
    slot: int = None

    idTobjId = list()
    tObjId = None # forgein Key ProfinetSystem
    NetworkInterfaces = list()

    def __repr__(self):
        return self.name

