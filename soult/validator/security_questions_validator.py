from schema import Schema, And, SchemaError

def validate(data: list) -> list:
    errors = []

    schema = Schema(And(
            list,
            lambda lst: all(isinstance(q, dict) for q in lst),  # Each item must be a dict
            lambda lst: all('question' in q and 'answer' in q for q in lst),  # Must have 'question' & 'answer'
            lambda lst: all(isinstance(q['question'], str) and isinstance(q['answer'], str) for q in lst),  # Both should be strings
        )
    )

    try:
        return schema.validate(data)  # Validate the data
    except SchemaError as e:
        errors.append(str(e))

    if errors:
        return [{"errors":["data is in wrong format"]}]