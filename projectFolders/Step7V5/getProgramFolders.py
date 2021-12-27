from DBF import ParseDBF
from collections import OrderedDict
from .s7ProgrammFolder import S7ProgrammFolder




def getAllProgramFolders(projectfolder):
    file = projectfolder + "\\" + "hrs" + "\\" + "S7RESOFF.DBF"
    dbf = ParseDBF(file)
    ProgramFolders = list()

    for record in dbf.getColumns(["ID", "NAME", "RSRVD4_L"], "ISO-8859-1"):
        folder = S7ProgrammFolder()
        folder.Name = record["NAME"]
        folder._linkfileoffset = int(record["RSRVD4_L"])
        folder.ID = int(record["ID"])
        ProgramFolders.append(folder)


    return ProgramFolders
