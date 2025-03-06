from utils.response_utils import build_response

def test_build_response_with_valid_data():
    data = {"key": "value"}
    response = build_response(data)
    assert response == {"data": data}

def test_build_response_with_empty_data():
    response = build_response({})
    assert response == {"data": {}}

def test_build_response_with_none():
    response = build_response(None)
    assert response == {"data": None}

def test_build_response_with_list():
    data = [1, 2, 3]
    response = build_response(data)
    assert response == {"data": [1, 2, 3]}

def test_build_response_with_string():
    response = build_response("test_string")
    assert response == {"data": "test_string"}
