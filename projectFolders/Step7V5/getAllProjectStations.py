from DBF import ParseDBF
from datatypes import StationType, StationConfigurationFolder


def getAllProjectStations(parent=None, projectFolder=None):
    # if projectFolder, use projectfolder, else use parent.projectFolder
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hstatx\\HOBJECT1.DBF")
    stations = dict()

    for row in dbf.records:
        if StationType.has_value(int(row["OBJTYP"])):
            station = StationConfigurationFolder()
            station.Name = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
            station.ID = int(row["ID"])
            station.UnitID = int(row["UNITID"])
            station.ObjTyp = int(row["OBJTYP"])
            station.parent = parent
            station.stationType = int(row["OBJTYP"])
            stations[station.ID] = station
    return stations
