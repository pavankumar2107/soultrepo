from schema import Schema, And, Optional
import re
from utils.validator_utils import validate_field_dict

def validate(loved_ones_data: dict) -> dict:
    schema = Schema({
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(str,len,error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(str,len,error="Field 'updated_at' should be a non-empty string"),
        Optional('status'): And(bool,error="Field 'status' should be a boolean"),
        Optional('first_name'): And(str, len, error="Field 'first_name' should be a non-empty string"),
        Optional('maiden_name'):  And(str,len,error="Field 'maiden_name' should be a non-empty string"),
        Optional('last_name'):  And(str,len,error="Field 'last_name' should be a non-empty string"),
        Optional('relationship'):  And(str,len,error="Field 'relationship' should be a non-empty string"),
        Optional('role'):  And(str,len,error="Field 'role' should be a non-empty string"),
        Optional('phone_number'): Optional(And(str, len, lambda s: len(s) == 10 and s.isdigit(), error="Phone number must be a 10-digit number")),
        Optional('gender'): And(str,len,error="Field 'gender' should be a non-empty string"),
        Optional('email_id'): Optional(And(str, lambda s: bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', s)), error="Invalid email format")),
        Optional('address'):  And(str,len,error="Field 'address' should be a non-empty string"),
        Optional('dob'):  And(str,len,error="Field 'dob' should be a non-empty string"),
        Optional('aadhar_number'): And(str, lambda n: len(str(n)) == 12, error="Aadhar number must be 12 digits")
    })

    errors = list(filter(None, map(lambda key: validate_field_dict(key, loved_ones_data[key], schema), loved_ones_data)))
    return loved_ones_data if not errors else {"errors": errors}


