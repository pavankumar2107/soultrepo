from fastapi.testclient import TestClient
from unittest.mock import patch
from router.financial_asset_router import router

client = TestClient(router)

@patch("handler.financial_asset_handler.find")
def test_get_financial_asset_success(mock_find):
    mock_find.return_value = {"id": "fa123", "name": "Stocks"}
    response = client.get("/user/124/financial_asset/fa123")
    assert response.status_code == 200
    assert response.json() == {"id": "fa123", "name": "Stocks"}
    mock_find.assert_called_once_with("124", "fa123")

@patch("handler.financial_asset_handler.find_all")
def test_get_all_financial_assets_success(mock_find_all):
    mock_find_all.return_value = [{"id": "fa123", "name": "Stocks"}]
    response = client.get("/user/123/financial_asset/")
    assert response.status_code == 200
    assert response.json() == [{"id": "fa123", "name": "Stocks"}]
    mock_find_all.assert_called_once_with("123")

@patch("handler.financial_asset_handler.create")
def test_create_financial_asset_success(mock_create):
    mock_create.return_value = {"id": "fa123", "name": "NewAsset"}
    response = client.post("/user/123/financial_asset/", json={"name": "NewAsset"})
    assert response.status_code == 200
    assert response.json() == {"id": "fa123", "name": "NewAsset"}
    mock_create.assert_called_once_with("123", {"name": "NewAsset"})

@patch("handler.financial_asset_handler.update")
def test_update_financial_asset_success(mock_update):
    mock_update.return_value = {"id": "fa123", "name": "UpdatedAsset"}
    response = client.put("/user/123/financial_asset/fa123", json={"name": "UpdatedAsset"})
    assert response.status_code == 200
    assert response.json() == {"id": "fa123", "name": "UpdatedAsset"}
    mock_update.assert_called_once_with("123", "fa123", {"name": "UpdatedAsset"})

@patch("handler.financial_asset_handler.delete")
def test_delete_financial_asset_success(mock_delete):
    mock_delete.return_value = {"message": "Financial asset deleted"}
    response = client.delete("/user/123/financial_asset/fa123")
    assert response.status_code == 200
    assert response.json() == {"message": "Financial asset deleted"}
    mock_delete.assert_called_once_with("123", "fa123")
