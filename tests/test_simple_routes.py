from tests.conftest import client


def test_index():
    response = client.get("/")

    assert {"Hello": "World"} == response.json()
