from schema import Schema, And, Optional
from utils.validator_utils import validate_field_dict

def validate(organ_donation_preference: dict) -> dict:
    # Define the schema
    schema = Schema({
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'):And(str, len, error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(str, len, error="Field 'updated_at' should be a non-empty string"),
        Optional('status'): And(bool ,error="Field 'status' should be a boolean"),
        Optional("organ"): And(str, len, error="Field 'organ' should be a string"),
        Optional("additional_conditions"): And(str, len, error="Field 'additional_conditions' should be a string"),
    })

    # Validate each field using map() and lambda
    errors = list(filter(None, map(lambda key: validate_field_dict(key, organ_donation_preference[key], schema),
                                   organ_donation_preference)))
    return organ_donation_preference if not errors else {"errors": errors}