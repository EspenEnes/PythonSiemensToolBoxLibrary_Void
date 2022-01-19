from .stationTypes import StationType
from .cpuType import PLCType


class StationConfigurationFolder():
    def __init__(self):
        self.parent = None
        self.UnitID = None
        self._objTyp = None
        self._stationType = None
        self.modules = list()

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