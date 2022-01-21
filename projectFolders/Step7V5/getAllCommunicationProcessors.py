from DBF import ParseDBF
from dbfread import exceptions
from datatypes import CpFolder
from projectFiles import Step7ProjectV5


def getAllCommunicationProcessors(parent:Step7ProjectV5=None, projectFolder=None):
    # if projectFolder, use projectfolder, else use parent.projectFolder
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    root = f"{projectFolder}\\hOmSave7\\s7wb53ax"
    file = f"{root}\\HOBJECT1.DBF"
    folders = {}
    try:
        dbf = ParseDBF(file)
    except exceptions.DBFNotFound:
        return folders

    for row in dbf.records:
        cp = CpFolder()

        cp.ID = int(row["ID"])

        cp.unitID = int(row["UNITID"])
        cp.objTyp = int(row["OBJTYP"])

        cp.name = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
        cp.rack = int(row["SUBSTATN"])
        cp.slot = int(row["MODULN"])
        cp.subModulNumber = int(row["SUBMODN"])
        folders[cp.ID] = cp

    root = f"{projectFolder}\\hOmSave7\\s7wb53ax"
    file = f"{root}\\HRELATI1.DBF"
    dbf = ParseDBF(file)


    for row in dbf.records:
        if int(row["RELID"]) == 1315827: #Add CP to Station
            STATION = next((station for station in parent.station.values() if station.ID == int(row["TUNITID"])), None)
            CP = next((cp for cp in folders.values() if cp.ID == int(row["SOBJID"])), None)
            if STATION and CP:
                STATION.modules.append(CP)
                CP.parent = STATION
        elif int(row["RELID"]) == 64: #Add NetworkInterface Foreign key to CP
            CP = next((cp for cp in folders.values() if cp.ID == int(row["SOBJID"])), None)
            if CP:
                CP.tObjId = int(row["TOBJID"])
    return folders
