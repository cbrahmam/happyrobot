import pytest
from fastapi.testclient import TestClient

def test_get_load_by_reference(client):
    """Test getting a load by reference number"""
    response = client.get("/api/loads/L789123")
    assert response.status_code == 200
    data = response.json()
    assert data["reference_number"] == "L789123"
    assert data["origin"] == "Menasha WI"
    assert data["destination"] == "Ada MI"

def test_search_loads(client):
    """Test searching loads with criteria"""
    response = client.get(
        "/api/loads/search",
        params={
            "origin": "Chicago",
            "equipment_type": "Van"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1  # We have L789126 in Chicago
    assert len(data["loads"]) >= 1
    assert "Chicago" in data["loads"][0]["origin"]

def test_load_not_found(client):
    """Test handling of non-existent load"""
    response = client.get("/api/loads/NONEXISTENT")
    assert response.status_code == 404

def test_search_no_results(client):
    """Test search with no matching results"""
    response = client.get(
        "/api/loads/search",
        params={
            "origin": "NonExistentCity",
            "destination": "NowhereVille"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["loads"]) == 0