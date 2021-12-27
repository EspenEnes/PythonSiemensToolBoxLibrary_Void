import re
from SimaticTools.datatypes import EthernetNetworkInterface, MpiProfibusNetworkInterface



class Interface():
    def __init__(self, projectfolder):
        self.projectfolder = projectfolder
        self.completeBuffer = self._readInterfaceFile(projectfolder)

    def getIpInterface(self):
        Interfaces = []
        matchesIpStructure = re.compile(b'\x03\x52\x14\x00').finditer(self.completeBuffer)

        for structure in matchesIpStructure:
            ethernet = EthernetNetworkInterface()
            struct = self.completeBuffer[structure.end(0): structure.end(0) + 1705]
            ethernet.IPAddress = self.getIP(struct)
            ethernet.SubnetMask = self.getMask(struct)
            ethernet.PhysicalAddress = self.getMac(struct)
            ethernet.IPAddressRouter = self.getRouter(struct)
            ethernet.UseRouter = self.getUseRouter(struct)
            ethernet.UseIp = self.getUseIp(struct)
            ethernet.UseIso = self.getUseMAC(struct)

            Interfaces.append(ethernet)
        return Interfaces

    def _readInterfaceFile(self, projectfolder):
        file = projectfolder + "\\" + "S7Netze" + "\\" + "S7NONFGX.tab"
        try:
            f = open(file, "rb")
            data = f.read()
            f.close()
        except IOError:
            data = None
        return data

    def getIP(self, struct):
        matchesIP = re.compile(b'\xE0\x0F\x00\x00\xE0\x0F\x00\x00').finditer(struct)
        for matchIP in matchesIP:
            IPhex = struct[matchIP.end(0) + 21: matchIP.end(0) + 21 + int(struct[matchIP.end(0) + 20])]
            IP = f"{int(IPhex[0:2], 16)}.{int(IPhex[2:4], 16)}.{int(IPhex[4:6], 16)}.{int(IPhex[6:8], 16)}"
            return IP

    def getMask(self, struct):
        matchesMask = re.compile(b'\xE5\x0F\x00\x00\xE5\x0F\x00\x00').finditer(struct)
        for matchMask in matchesMask:
            maskHex = struct[matchMask.end(0) + 21: matchMask.end(0) + 21 + int(struct[matchMask.end(0) + 20])]
            mask = f"{int(maskHex[0:2], 16)}.{int(maskHex[2:4], 16)}.{int(maskHex[4:6], 16)}.{int(maskHex[6:8], 16)}"
            return mask

    def getMac(self, struct):
        matchesMAC = re.compile(b'\xA2\x0F\x00\x00\xA2\x0F\x00\x00').finditer(struct)
        for matchMAC in matchesMAC:
            MAChex = struct[matchMAC.end(0): matchMAC.end(0) + 21 + int(struct[matchMAC.end(0) + 20])]
            return MAChex

    def getRouter(self, struct):
        matchesRouter = re.compile(b'\xE3\x0F\x00\x00\xE3\x0F\x00\x00').finditer(struct)
        for matchRouter in matchesRouter:
            routerHex = struct[
                        matchRouter.end(0) + 21: matchRouter.end(0) + 21 + int(struct[matchRouter.end(0) + 20])]
            router = f"{int(routerHex[0:2], 16)}.{int(routerHex[2:4], 16)}.{int(routerHex[4:6], 16)}.{int(routerHex[6:8], 16)}"
            return router

    def getUseRouter(self, struct):
        matchesUseRouter = re.compile(b'\xE8\x0F\x00\x00\xE8\x0F\x00\x00').finditer(struct)
        for matchUseRouter in matchesUseRouter:
            useRouter = bool(matchUseRouter.end(0) + 20)
            return useRouter

    def getUseIp(self, struct):
        matchesUseIP = re.compile(b'\xEa\x0F\x00\x00\xEA\x0F\x00\x00').finditer(struct)
        for matcheUseIP in matchesUseIP:
            useIp = bool(matcheUseIP.end(0) + 20)
            return useIp

    def getUseMAC(self, struct):
        matchesUseMAC = re.compile(b'\xED\x0F\x00\x00\xED\x0F\x00\x00').finditer(struct)
        for matcheUseMAC in matchesUseMAC:
            useMAC = bool(matcheUseMAC.end(0) + 20)
            return useMAC




    def getMpiInterface(self):
        Interfaces = []
        matchesMPIStructure = re.compile(b'\x01\x52\x14\x00').finditer(self.completeBuffer)

        for structure in matchesMPIStructure:
            struct = self.completeBuffer[structure.end(0): structure.end(0) + 2001]

            matchesMPI = re.compile(b'\x9A\x08\x00\x00\x9A\x08\x00\x00').finditer(struct)
            for matchMPI in matchesMPI:
                MPI = MpiProfibusNetworkInterface()
                MPI.NetworkInterfaceType = "MPI"
                MPI.Address = int(struct[matchMPI.end(0) + 17])
                Interfaces.append(MPI)
            return Interfaces

    def getDpInterface(self):
        Interfaces = []
        matchesDPStructure = re.compile(b'\x02\x52\x14\x00').finditer(self.completeBuffer)

        for structure in matchesDPStructure:
            struct = self.completeBuffer[structure.end(0): structure.end(0) + 2001]

            matchesDP = re.compile(b'\x36\x08\x00\x00\x36\x08\x00\x00').finditer(struct)
            for matchDP in matchesDP:
                DP = MpiProfibusNetworkInterface()
                DP.NetworkInterfaceType = "DP"
                DP.Address = int(struct[matchDP.end(0) + 17])
                Interfaces.append(DP)
            return Interfaces






