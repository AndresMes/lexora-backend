from enum import Enum

class PartyType(str, Enum):
    DISTRIBUTOR = "DISTRIBUTOR"
    CLIENT = "CLIENT"