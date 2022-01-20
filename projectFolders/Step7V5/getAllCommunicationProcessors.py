from DBF import ParseDBF
from dbfread import exceptions
from datatypes import CpFolder


def getAllCommunicationProcessors(parent=None, projectFolder=None):
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

    return folders
