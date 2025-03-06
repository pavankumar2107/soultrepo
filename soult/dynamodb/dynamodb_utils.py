from enum import Enum
class Entity(Enum):
    ELP = "end_life_preferences"
    FA = "assets"
    LO = "loved_ones"
    NMM = "non_material_assets"
    ODP = "organ_donation_preferences"
    SQ = "security_questions"
    EMPLOYEE = "employee"
    AUDIT_LOG = "audit_log"



def get_expression(e: Entity):
    return f'SET #{e.value} = list_append(if_not_exists(#{e.value}, :default), :{e.value})'