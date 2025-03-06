from schema import Schema, And, Optional
from utils.validator_utils import validate_field_dict

def validate(financial_asset_data: dict) -> dict:
    schema = Schema({
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(str, len, error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(str, len, error="Field 'updated_at' should be a non-empty string"),
        Optional('status'): And(bool, error="Field 'status' should be a boolean"),
        Optional('type'): And(str, len, error="Field 'type' should be non-empty string"),
        Optional('fund_name'): And(str, len, error="Field 'fund_name' should be non-empty string"),
        Optional('maturity_date'): And(str, len, error="Field 'maturity_date' should be a non-empty string"),
        Optional('details'):And(str, len, error="Field 'details' should be a non-empty string"),
        Optional('document_arn'):And(str, len, error="Field 'document_arn' should be a non-empty string"),
        Optional('nominees'): [
            {
                Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
                Optional('loved_one_id'): And(str, len, error="Field 'loved_one_id' should be a non-empty string"),
                Optional('share'): And(int, error="Field 'share' should be a integer"),
            }
        ],
    })

    errors = list(filter(None, map(lambda key: validate_field_dict(key, financial_asset_data[key], schema), financial_asset_data)))
    return financial_asset_data if not errors else {"errors": errors}
