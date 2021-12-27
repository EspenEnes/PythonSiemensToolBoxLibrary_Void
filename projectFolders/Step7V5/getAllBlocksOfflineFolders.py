from DBF import ParseDBF
from .blockOfflineFolder import BlockOfflineFolder


def getAllBlocksOfflineFolders(projectFolder, encoding):
        root = f"{projectFolder}\\ombstx\\offline"
        file = f"{root}\\BSTCNTOF.DBF"
        dbf = ParseDBF(file)

        folders = list()
        for record in dbf.records:
                OfflineFolder = BlockOfflineFolder()
                OfflineFolder.name = record["NAME"]
                OfflineFolder.folder = root +"\\" + f"{int(record['ID']):08x}"
                OfflineFolder.ID = int(record["ID"])
                folders.append(OfflineFolder)
        return folders



