from DBF import ParseDBF
from datatypes.cpuFolder import CPUFolder
import os
from datatypes import PLCType, StationConfigurationFolder

#todo: Needs refactoring, duplicate codes


def getAllCpuFolders(parent=None, projectFolder=None):
    # if projectFolder, use projectfolder, else use parent.projectFolder
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    stations = parent._stations



    cpufolders = {}

    """CPU MpiDp 300 Folders"""
    if os.path.isfile(f"{projectFolder}\\hOmSave7\\s7hk31ax\\HRELATI1.DBF"):
        dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hk31ax\\HRELATI1.DBF")
        for station in stations.values():
            station : StationConfigurationFolder
            for row in dbf.records:
                if int(row["TOBJTYP"]) == station.stationType.value and int(row["TOBJTYP"]) == (PLCType.Simatic300.value or PLCType.SimaticRTX.value):
                    cpu = CPUFolder()
                    cpu.tObjTyp = int(row["TOBJTYP"])
                    cpu.tObjId = int(row["TOBJID"])
                    cpu.unitID = int(row["TUNITID"])
                    cpu.cpuType = PLCType.Simatic300
                    cpu.ID = int(row["SOBJID"])
                    cpu.parent = station
                    station.modules.append(cpu)
                    cpufolders[cpu.ID] = cpu



    """CPU 300 ET200s Folders"""
    if os.path.isfile(f"{projectFolder}\\hOmSave7\\s7hkcomx\\HRELATI1.DBF"):
        dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hkcomx\\HRELATI1.DBF")

        for station in stations.values():
            station: StationConfigurationFolder
            for row in dbf.records:
                if int(row["TOBJTYP"]) == station.stationType.value and int(row["TOBJTYP"]) == PLCType.MpiDPinCPU.value:
                    cpu = CPUFolder()
                    cpu.tObjTyp = int(row["TOBJTYP"])
                    cpu.tObjId = int(row["TOBJID"])
                    cpu.unitID = int(row["TUNITID"])
                    cpu.cpuType = PLCType.Simatic300
                    cpu.ID = int(row["SOBJID"])
                    cpu.parent = station
                    station.modules.append(cpu)
                    cpufolders[cpu.ID] = cpu

    """CPU 400 Folders"""
    if os.path.isfile(f"{projectFolder}\\hOmSave7\\s7hk41ax\\HRELATI1.DBF"):
        dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hk41ax\\HRELATI1.DBF")

        for station in stations.values():
            station: StationConfigurationFolder
            for row in dbf.records:

                if int(row["TOBJTYP"]) == station.stationType.value and  (int(row["TOBJTYP"]) == PLCType.Simatic400.value or  int(row["TOBJTYP"]) == PLCType.Simatic400H.value):
                    cpu = CPUFolder()
                    cpu.tObjTyp = int(row["TOBJTYP"])
                    cpu.tObjId = int(row["TOBJID"])
                    cpu.unitID = int(row["TUNITID"])
                    cpu.cpuType = station.stationType
                    cpu.ID = int(row["SOBJID"])
                    cpu.parent = station
                    station.modules.append(cpu)
                    cpufolders[cpu.ID] = cpu



    """ Get The CPU(ET200S)"""
    if os.path.isfile(f"{projectFolder}\\hOmSave7\\s7hkcomx\\HOBJECT1.DBF"):
        dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hkcomx\\HOBJECT1.DBF")

        for row in dbf.records:
            try:
                cpu = cpufolders[int(row["ID"])]
                cpu.name = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
                cpu.rack = int(row["SUBSTATN"])
                cpu.slot = int[row["MODULN"]]
            except KeyError:
                pass

    """ Get The CPU(300)..."""
    if os.path.isfile(f"{projectFolder}\\hOmSave7\\s7hk31ax\\HOBJECT1.DBF"):
        dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hk31ax\\HOBJECT1.DBF")

        for row in dbf.records:
            try:
                cpu = cpufolders[int(row["ID"])]
                cpu.name = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
                cpu.rack = int(row["SUBSTATN"])
                cpu.slot = int(row["MODULN"])
            except KeyError:
                pass


    """ Get The CPU(400)..."""
    if os.path.isfile(f"{projectFolder}\\hOmSave7\\s7hk41ax\\HOBJECT1.DBF"):
        dbf = ParseDBF(f"{projectFolder}\\hOmSave7\\s7hk41ax\\HOBJECT1.DBF")

        for row in dbf.records:
            # print(row)

            try:
                cpu = cpufolders[int(row["ID"])] #todo: sjekk om 400cpu
                cpu.name = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
                cpu.rack = int(row["SUBSTATN"])
                cpu.slot = int(row["MODULN"])
            except KeyError:
                pass
    return cpufolders






