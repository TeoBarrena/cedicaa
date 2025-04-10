from tests import client

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert b"inicio" in response.data