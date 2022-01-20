from dataclasses import dataclass


@dataclass
class CPUFolder:
    parent = None
    unitID = None
    tObjTyp = None
    tObjId = None
    cpuType = None
    rack = None
    slot = None
    ID = None
    name = None
    idTobjID = list()

    NetworkInterfaces = list()
    subItems = list()

    def __repr__(self):
        return self.name
