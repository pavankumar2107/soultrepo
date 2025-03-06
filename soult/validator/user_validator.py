from schema import Schema, And, Optional
import re
from utils.validator_utils import  validate_field_dict


def validate(user: dict) -> dict:
    schema = Schema({
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(str, len, error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(str, len, error="Field 'updated_at' should be a non-empty string"),
        Optional('status'): And(bool, error="Field 'status' should be a boolean"),
        Optional('firstname'): And(str, len, error="Field 'firstname' should be a non-empty string"),
        Optional('lastname'): And(str, len, error="Field 'lastname' should be a non-empty string"),
        Optional('phone_no'): (And(str, len, lambda s: len(s) == 10 and s.isdigit(), error="Phone number must be a 10-digit number")),
        Optional('email'): And(str, lambda s: bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', s)), error="Invalid email format"),
        Optional('address'): And(str, len, error="Field 'address' should be a non-empty string"),
        Optional('dob'): And(str, len, error="Field 'dob' should be a non-empty string"),
        Optional('gender'): And(str, len, error="Field 'gender' should be a non-empty string"),
        Optional('mpin'): And(str, len, error="Field 'mpin' should be a non-empty string"),
    })

    errors = list(filter(None, map(lambda key: validate_field_dict(key, user[key], schema),user)))
    return user if not errors else {"errors": errors}