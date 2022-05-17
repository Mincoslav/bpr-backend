import json
from datetime import datetime
from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
import app


client = TestClient(app.app)


def test_read_root():

    response = client.get("/")
    print(response.content)
    assert response.status_code == 200
    assert response.json() == {"Hello": "Bachelors"}


def test_get_danger_zones():

    response = client.get("/danger_zones/")
    assert response.status_code == 200
    assert response.json() == {
        "message": HTTP_200_OK,
        "danger_zones": [
            {
                "location": {"type": "Point", "coordinates": [55.863649, 9.837673]},
                "last_updated": "2022-04-16T12:29:30.671000",
                "country": "Denmark",
                "radius": 100,
                "_id": "626fbeae0edad4e3f317fd77",
            },
            {
                "location": {
                    "type": "Point",
                    "coordinates": [55.86127015158933, 9.853120557561514],
                },
                "last_updated": "2022-04-16T12:29:30.671000",
                "country": "Denmark",
                "radius": 250,
                "_id": "626fbee40edad4e3f317fd78",
            },
        ],
    }


def test_post_create_alert():
    data = {
        "country": "Denmark",
        "last_updated": datetime.now().timestamp(),
        "location": {"coordinates": [9.8381103, 55.8639916], "type": "Point"},
        "resolved": False,
        "responderID": "",
        "status": "received",
        "userID": "sJc8KRF9PwMsF8d34PLVlbgPoLD2",
    }
    response = client.post(
        url="/create_alert/",
        data=json.dumps(data),
    )
    assert response.status_code == 201
    assert response.json() == {
        "response": HTTP_201_CREATED,
        "message": "alert created",
    }


def test_post_create_alert_wrong_format_error():
    data = {
        "country": "Denmark",
        "last_updated": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "location": {"coordinates": [9.8381103, 55.8639916], "type": "Point"},
        "resolved": False,
        "responderID": "",
        "status": "received",
        "userID": "sJc8KRF9PwMsF8d34PLVlbgPoLD2",
    }
    response = client.post(
        url="/create_alert/",
        data=json.dumps(data),
    )
    assert response.status_code == 422


def test_post_nearest_responder():
    data = {
        "userID": "3cGGYEi5GxyROvKRHQPK7Irvy1",
        "location": {"type": "Point", "coordinates": [9.838969, 55.863775]},
        "last_updated": datetime.now().timestamp(),
        "country": "Denmark",
        "expo_token": "ExponentPushToken[bhz8GWJ9N98LtKk_fN3My1]",
    }
    response = client.post(url="/nearest_responder/", data=json.dumps(data))
    assert response.status_code == HTTP_200_OK


def test_post_nearest_responder_wrong_format_error():
    data = {
        "userID": "3cGGYEi5GxyROvKRHQPK7Irvy1",
        "location": {"type": "Point", "coordinates": [9.838969, 55.863775]},
        "last_updated": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "country": "Denmark",
        "expo_token": "ExponentPushToken[bhz8GWJ9N98LtKk_fN3My1]",
    }
    response = client.post(url="/nearest_responder/", data=json.dumps(data))
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_post_responders_within_range():
    data = {
        "userID": "3cGGYEi5GxyROvKRHQPK7Irvy1",
        "location": {"type": "Point", "coordinates": [9.838969, 55.863775]},
        "last_updated": datetime.now().timestamp(),
        "country": "Denmark",
        "expo_token": "ExponentPushToken[bhz8GWJ9N98LtKk_fN3My1]",
    }
    response = client.post(url="/responders_within_range/", data=json.dumps(data))

    assert response.status_code == HTTP_200_OK


def test_post_responders_within_range_wrong_param_error():
    data = {
        "userID": "3cGGYEi5GxyROvKRHQPK7Irvy1",
        "location": {"type": "Point", "coordinates": [9.848969, 55.863775]},
        "last_updated": datetime.now().timestamp(),
        "country": "Denmark",
        "expo_token": "ExponentPushToken[bhz8GWJ9N98LtKk_fN3My1]",
    }
    print(json.dumps(data))
    response = client.post(url="/responders_within_range/?distance=0", data=json.dumps(data))

    assert response.status_code == HTTP_404_NOT_FOUND


def test_post_responders_within_range_wrong_format_error():
    data = {
        "userID": "3cGGYEi5GxyROvKRHQPK7Irvy1",
        "location": {"type": "Point", "coordinates": [9.838969, 55.863775]},
        "last_updated": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "country": "Denmark",
        "expo_token": "ExponentPushToken[bhz8GWJ9N98LtKk_fN3My1]",
    }
    response = client.post(url="/responders_within_range/", data=json.dumps(data))

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_put_update_location():
    assert True


def test_put_accept_alert():
    assert True
