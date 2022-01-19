import enum


class PLCType(enum.Enum):
    Simatic300 = 1314969
    Simatic400 = 1314970
    Simatic400H = 1315650
    Simatic400H_backup = 1315656
    SimaticRTX = 1315651
    EternetInCPU3xx = 2364796
    EternetInCPU3xx_2 = 2364572
    EternetInCPU3xxF = 2364818
    EternetInCPU4xx = 2364763
    EternetInCPURTX = 2364315
    MpiDPinCPU = 1314972
    MpiDP400 = 1315038
    MpiDP300 = 1315016
