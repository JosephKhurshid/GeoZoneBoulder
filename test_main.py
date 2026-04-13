from fastapi.testclient import TestClient
from main import app

def test_api():
    with TestClient(app) as client:
        
        address = "2635 MAPLETON AVE"        
        #making sure this returns a 200 msg and the right fields. And cache miss
        response_one = client.get(f"/api/v1/zoning?address={address}")
        assert response_one.status_code == 200
        
        data_one = response_one.json()
        assert data_one["address"] == address
        assert "zoning_code" in data_one
        assert "zoning_description" in data_one
        assert "zoning_purpose" in data_one
        assert data_one["source"] == "PostGIS Database"

        #reddis cahche hit test
        response_two = client.get(f"/api/v1/zoning?address={address}")
        assert response_two.status_code == 200
        
        data_two = response_two.json()
        assert data_two["source"] == "Redis Cache" 

        #making sure I get a 404
        bad_address = "789 Colfax Ave, Denver, CO"
        response_bad = client.get(f"/api/v1/zoning?address={bad_address}")
        
        assert response_bad.status_code == 404
        assert response_bad.json()["detail"] == "Address not found or outside zoning boundaries."