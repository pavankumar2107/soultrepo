from schema import Schema, And, Optional
from utils.validator_utils import validate_field

def validate(end_life_preferences: dict) -> dict:
    schema_dict = {
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(str),
        Optional('updated_at'): And(str),
        Optional('status'): And(bool, error="Field 'status' should be a boolean"),
        Optional("resuscitation"): And(str, len, error="Field 'resuscitation' should be a string"),
        Optional("condition_for_withdrawal"): And(str, len, error="Field 'condition_for_withdrawal' should be a string"),
        Optional("ventilator"): And(str, len, error="Field 'ventilator' should be a string"),
        Optional("duration_of_support"): And(int, error="Field 'duration_of_support' should be an integer"),
        Optional("decision_maker"): {
            Optional('id'): And(str, len, error="Field 'decision_maker.id' should be a string"),
            Optional("type_of_decision_maker"): And(str, len, error="Field 'decision_maker.type_of_decision_maker' should be a string"),
        }
    }

    Schema(schema_dict)  # Validate schema structure

    def get_field_schema(key, schema_obj):
        """Retrieve the schema definition for a given key."""
        return next(
            (schema_obj[sk] for sk in schema_obj if (isinstance(sk, Optional) and sk.schema == key) or sk == key),
            None
        )

    def validate_key_value(key, value, schema_obj):
        """Recursively validate key-value pairs based on schema rules."""
        field_schema = get_field_schema(key, schema_obj)

        if isinstance(value, dict) and isinstance(field_schema, dict):
            nested_schema = field_schema
            return sum(
                map(lambda k: validate_key_value(k, value.get(k), nested_schema), value.keys()), []
            )

        return list(filter(None, [validate_field(key, value, {key: field_schema})] if field_schema else []))

    errors = list(filter(None, sum(
        map(lambda k: validate_key_value(k, end_life_preferences.get(k), schema_dict), end_life_preferences.keys()),
        []
    )))

    return end_life_preferences if not errors else {"errors": errors}