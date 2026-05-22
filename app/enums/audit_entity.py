from enum import Enum


class AuditEntity(str, Enum):
    USER = "USER"
    PARTY = "PARTY"
    INVOICE = "INVOICE"