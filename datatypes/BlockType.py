import enum


class BlockType(enum.Enum):
    AllBlocks = 0xffff
    AllEditableBlocks = 0xfffe
    SourceBlock = 2

    # Step7 Types...
    OB = 0x08  # 8
    DB = 0x0a  # 10
    SDB = 0x0b  # 11
    FC = 0x0c  # 12
    SFC = 0x0d  # 13
    FB = 0x0e  # 14
    SFB = 0x0f  # 15
    UDT = 0x00  # 0
    VAT = 0x1B  # 27

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


def BlockTypeString(blockType):
    if blockType == BlockType.DB:
        return "Datablock"
    elif blockType == BlockType.FB:
        return "Functionblock"
    elif blockType == BlockType.FC:
        return "Function"
    elif blockType == BlockType.OB:
        return "Organisationblock"
    elif blockType == BlockType.UDT:
        return "Userdatatype"
    elif blockType == BlockType.VAT:
        return "Variabletable"
    elif blockType == BlockType.SFC:
        return "Systemfunction"
    elif blockType == BlockType.S5_DB:
        return "S5-Datablock"
    elif blockType == BlockType.S5_FB:
        return "S5-Functionblock"
    elif blockType == BlockType.S5_PB:
        return "S5-Programblock"
    elif blockType == BlockType.S5_FX:
        return "S5-ExtenedFunctionblock"
    elif blockType == BlockType.S5_SB:
        return "S5-Stepblock"
    elif blockType == BlockType.S5_DV:
        return "S5-Datablock-Preheader"
    elif blockType == BlockType.S5_FV:
        return "S5-Functionblock-Preheader"
    elif blockType == BlockType.S5_FVX:
        return "S5-Extendedfunctionblock-Preheader"
    elif blockType == BlockType.S5_DX:
        return "S5-Extendeddatablock"
    elif blockType == BlockType.S5_DVX:
        return "S5-Extendeddatablock-Preheader"
    elif blockType == BlockType.S5_OB:
        return "S5-Organisationblock"
    elif blockType == BlockType.S5_PK:
        return "S5-Programcommentblock"
    elif blockType == BlockType.S5_FK:
        return "S5-Functioncommentblock"
    elif blockType == BlockType.S5_FKX:
        return "S5-Extendedfunctioncommentblock"
    elif blockType == BlockType.S5_SK:
        return "S5-Stepcommentblock"
    elif blockType == BlockType.S5_DK:
        return "S5-Datacommentblock"
    elif blockType == BlockType.S5_DKX:
        return "S5-Extendeddatacommentblock"
    elif blockType == BlockType.S5_OK:
        return "S5-Organisationcommentblock"
    elif blockType == BlockType.S5_BB:
        return "S5-Variabletable"
    elif blockType == BlockType.SourceBlock:
        return "Sourceblock"
    return ""
