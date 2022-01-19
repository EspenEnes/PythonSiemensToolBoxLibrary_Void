import enum



class StationType(enum.Enum):
    Simatic300 = 1314969
    Simatic400 = 1314970
    Simatic400H = 1315650
    SimaticPC = 1315651

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_




