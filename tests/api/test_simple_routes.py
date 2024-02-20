from fastapi.testclient import TestClient


def test_index(client: TestClient):
    response = client.get("/")

    assert {"Hello": "World"} == response.json()
