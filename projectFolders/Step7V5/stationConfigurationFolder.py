from dataclasses import dataclass
from datatypes import PLCType, StationType


@dataclass
class StationConfigurationFolder:
    parent = None
    UnitID = None
    _objTyp = None
    _stationType = None
    modules = list()

    @property
    def stationType(self):
        return self._stationType

    @stationType.setter
    def stationType(self, value):
        if value == StationType.Simatic300.value:
            self._stationType = PLCType.Simatic300
        elif value == StationType.Simatic400.value:
            self._stationType = PLCType.Simatic400
        elif value == StationType.Simatic400H.value:
            self._stationType = PLCType.Simatic400H
        elif value == StationType.SIAMTICPC.value:
            self._stationType = PLCType.SimaticRTX

    def __repr__(self):
        return str(self._stationType)



