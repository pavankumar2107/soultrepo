from schema import Schema, And, Optional
from utils.validator_utils import  validate_field_dict


def validate(non_material_memory_data: dict) -> dict:
    schema = Schema({
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string  "),
        Optional('created_at'): And(str, len, error="Field 'created_at' should be a non-empty string  "),
        Optional('updated_at'): And(str, len, error="Field 'updated_at' should be a non-empty string  "),
        Optional('status'): And(bool ,error="Field 'status' should be a boolean"),
        Optional('non_asset_type'): And(str, len, error="Field 'non_asset_type' should be non-empty string"),
        Optional('details'): And(str, len, error="Field 'details' should be a non-empty string  "),
        Optional('memory'): [
            {
                Optional('id'): And(str, len, error="Field 'id' should be non-empty string"),
                Optional('type'): And(str, len, error="Field 'type' should be non-empty string"),
                Optional('created_at'): And(str, len, error="Field 'created_at' should be a non-empty string  "),
                Optional('status'):And(bool ,error="Field 'status' should be a boolean"),
                Optional('document_arn'): And(str, len, error="Field 'document_arn' should be non-empty string"),
            }
        ]
    })

    errors = list(filter(None, map(lambda key: validate_field_dict(key, non_material_memory_data[key], schema), non_material_memory_data)))
    return non_material_memory_data if not errors else {"errors": errors}