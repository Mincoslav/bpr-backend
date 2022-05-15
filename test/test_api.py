from fastapi.testclient import TestClient

import app


client = TestClient(app.app)


def test_read_root():

    response = client.get("/")
    print(response.content)
    assert response.status_code == 200
    assert response.json() == {"Hello": "Bachelors"}