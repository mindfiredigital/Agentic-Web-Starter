def test_health_success(client):
    """Verify /health returns 200 and expected message."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Up and running"}
