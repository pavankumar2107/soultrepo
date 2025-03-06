from schema import Schema, SchemaError

#if the Dictionaries contains child Dictionary
def validate_field(key, value, schema_obj):
    try:
        field_schema = Schema({key: schema_obj[key]})  # Use correct field schema
        field_schema.validate({key: value})
    except SchemaError as e:
        return str(e)  # Return error message
    return None


def validate_field_dict(key, value, schema):
    try:
        schema.validate({key: value})
    except SchemaError as e:
        return str(e)
    return None
