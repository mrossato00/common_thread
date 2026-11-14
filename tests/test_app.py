import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_home_ok(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"The Hobbit" in response.data


def test_work_page_shows_relations(client):
    response = client.get("/work/the-hobbit")
    assert response.status_code == 200
    assert b"prequel of" in response.data
    assert b"prequel_of" not in response.data


def test_unknown_work_is_404(client):
    response = client.get("/work/inesistente")
    assert response.status_code == 404


def test_search_no_results(client):
    response = client.get("/?q=xyz")
    assert response.status_code == 200
    assert b"No works found." in response.data