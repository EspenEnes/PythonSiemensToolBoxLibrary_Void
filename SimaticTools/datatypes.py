import enum

class  EthernetNetworkInterface():
    def __init__(self):
        self.NetworkInterfaceType = "IP"
        self.Name = None

        self.UseIso: bool = False
        self.PhysicalAddress: str = ""
        self.UseIp: bool = False
        self.IPAddress: str = ""
        self.SubnetMask: str = ""
        self.UseRouter: bool = False
        self.IPAddressRouter: str = ""

    def __str__(self):
        return (self.Name or "") + ", Ip: " + self.IPAddress

class MpiProfibusNetworkInterface():
    def __init__(self):
        self.NetworkInterfaceType = "MPI"
        self.Name = None

        self.Address = None

    def __str__(self):
        return f"{self.Name or ''} ({self.NetworkInterfaceType}) Adress: {self.Address}"


class PLCBlockType(enum.Enum):
    AllBlocks = 0xffff
    AllEditableBlocks = 0xfffe
    SourceBlock = 2

    # Step7 Types...
    OB = 0x08   #8
    DB = 0x0a   #10
    SDB = 0x0b  #11
    FC = 0x0c   #12
    SFC = 0x0d  #13
    FB = 0x0e   #14
    SFB = 0x0f  #15
    UDT = 0x00  #0
    VAT = 0x1B  #27

    # Step5 Types...
    S5_PB = 0xf04
    S5_FB = 0xf08
    S5_FX = 0xf05
    S5_DB = 0xf01
    S5_DX = 0xf0c
    S5_SB = 0xf02
    S5_OB = 0xf10
    S5_OK = 0xf51
    S5_PK = 0xf31
    S5_FK = 0xf41
    S5_FKX = 0xf5a
    S5_SK = 0xf21
    S5_DK = 0xf5b
    S5_DKX = 0xf5c
    S5_BB = 0xf64

    S5_FV = 0xff1
    S5_FVX = 0xff2
    S5_DV = 0xff3
    S5_DVX = 0xff4

    # TIA Portal7 Types...
    S7V11_OB = 0xe08
    S7V11_DB = 0xe0a
    S7V11_SDB = 0xe0b
    S7V11_FC = 0xe0c
    S7V11_SFC = 0xe0d
    S7V11_FB = 0xe0e
    S7V11_SFB = 0xe0f
    S7V11_UDT = 0xeff
    S7V11_VAT = 0xe1B


