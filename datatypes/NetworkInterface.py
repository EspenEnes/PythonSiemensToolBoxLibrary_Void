from dataclasses import dataclass

@dataclass
class  EthernetInterface:
    NetworkInterfaceType = "IP"
    Name = None
    UseIso: bool = False
    PhysicalAddress: str = ""
    UseIp: bool = False
    IPAddress: str = ""
    SubnetMask: str = ""
    UseRouter: bool = False
    IPAddressRouter: str = ""
    _id = None

    def __str__(self):
        return (self.Name or "") + ", Ip: " + self.IPAddress

    def __repr__(self):
        return (self.Name or "") + ", Ip: " + self.IPAddress


@dataclass
class MpiProfibusInterface:
    NetworkInterfaceType = "MPI"
    Name = None
    Address = None
    _id = None

    def __str__(self):
        return f"{self.Name or ''} ({self.NetworkInterfaceType}) Adress: {self.Address}"
