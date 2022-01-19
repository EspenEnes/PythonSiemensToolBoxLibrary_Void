from DBF import ParseDBF
from datatypes.s7ProgrammFolder import S7ProgrammFolder


def getAllProgramFolders(parent=None, projectFolder=None):
    # if projectFolder, use projectfolder, else use parent.projectFolder
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    programFolders = {}

    dbf = ParseDBF(fr"{projectFolder}\hrs\S7RESOFF.DBF")
    for row in dbf.records:
        folder = S7ProgrammFolder()
        folder.Name = row["NAME"].decode("ISO-8859-1").strip()
        folder._linkfileoffset = int(row["RSRVD4_L"])
        folder.ID = int(row["ID"])
        programFolders[folder.ID] = folder
    return programFolders
