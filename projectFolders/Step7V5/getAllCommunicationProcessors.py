import DBF
from DBF import ParseDBF
from dbfread import exceptions


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
        id = int(row["ID"])
        folders[id] = {}

        folders[id]["ID"] = id

        folders[id]["unitId"] = int(row["UNITID"])
        folders[id]["objTyp"] = int(row["OBJTYP"])

        folders[id]["name"] = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
        folders[id]["rack"] = int(row["SUBSTATN"])
        folders[id]["slot"] = int(row["MODULN"])
        folders[id]["subModulNumber"] = int(row["SUBMODN"])

    return folders
