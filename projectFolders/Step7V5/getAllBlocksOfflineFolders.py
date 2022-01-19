from DBF import ParseDBF
from .blockOfflineFolder import BlockOfflineFolder


def getAllBlocksOfflineFolders(parent=None, projectFolder=None):
    # if projectFolder, use projectfolder, else use parent.projectFolder
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    dbf = ParseDBF(fr"{projectFolder}\ombstx\offline\BSTCNTOF.DBF")

    folders = list()
    for row in dbf.records:
        OfflineFolder = BlockOfflineFolder()
        OfflineFolder.name = row["NAME"]
        OfflineFolder.folder = fr"{projectFolder}\ombstx\offline\{int(row['ID']):08x}"
        OfflineFolder.ID = int(row["ID"])
        folders.append(OfflineFolder)
    return folders
