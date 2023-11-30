from fastapi import Response
from fastapi.testclient import TestClient
from faas_demo import app

client = TestClient(app)

def test_get_chat():
    response: Response = client.post(
        "/get-chat",
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
