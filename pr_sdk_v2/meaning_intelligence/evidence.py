from enum import Enum
class EvidenceLevel(str, Enum):
    E0 = "E0"; E1 = "E1"; E2 = "E2"; E3 = "E3"
    E4 = "E4"; E5 = "E5"; E6 = "E6"
LEVEL_ORDER = {e: i for i, e in enumerate(EvidenceLevel)}
