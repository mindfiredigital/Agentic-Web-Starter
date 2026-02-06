def test_health_success(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Up and running"}
