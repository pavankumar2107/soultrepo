from utils.models import Model, Operation

def test_model_enum_values():
    assert Model.ELP.value == "END_LIFE_PREFERENCES"
    assert Model.NMM.value == "NON_MATERIAL_MEMORY"
    assert Model.FA.value == "FINANCIAL_ASSET"
    assert Model.LO.value == "LOVED_ONES"
    assert Model.USER.value == "USER"
    assert Model.ODP.value == "ORGAN_DONATION_PREFERENCES"
    assert Model.SQ.value == "SECURITY_QUESTION"


def test_operation_enum_values():
    assert Operation.CREATE.value == "CREATE"
    assert Operation.UPDATE.value == "UPDATE"
    assert Operation.DELETE.value == "DELETE"


def test_model_enum_membership():
    expected_models = {
        "ELP", "NMM", "FA", "LO", "USER", "ODP", "SQ"
    }
    actual_models = set(Model.__members__.keys())
    assert actual_models == expected_models


def test_operation_enum_membership():
    expected_operations = {"CREATE", "UPDATE", "DELETE"}
    actual_operations = set(Operation.__members__.keys())
    assert actual_operations == expected_operations


def test_enum_instance():
    assert isinstance(Model.USER, Model)
    assert isinstance(Operation.CREATE, Operation)

