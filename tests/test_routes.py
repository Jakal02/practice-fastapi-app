from tests.conftest import client


def test_index():
    response = client.get("/")

    assert {"Hello": "World"} == response.json()


def test_posts_root():
    response = client.get("/posts/")
    assert {"table": "posts"} == response.json()
