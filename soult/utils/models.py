from enum import Enum

class Model(Enum):
    ELP = "END_LIFE_PREFERENCES"
    NMM = "NON_MATERIAL_MEMORY"
    FA  = "FINANCIAL_ASSET"
    LO  = "LOVED_ONES"
    USER = "USER"
    ODP = "ORGAN_DONATION_PREFERENCES"
    SQ = "SECURITY_QUESTION"


class Operation(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

