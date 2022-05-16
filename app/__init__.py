# Comment this when running tests
from api_app import app

import azure.functions as func
from azure.functions import AsgiMiddleware
from fastapi import HTTPException, status
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from notifications import send_push_message
from payload_definitions import ButtonPressEvent, LatestLocation
from mongo_access_funcs import (
    get_danger_zones_documents,
    get_expo_token,
    get_nearest_responder_from_db,
    get_responders_within_range_from_db,
    post_document,
    update_location,
    accept_event_in_db,
)


tags_metadata = []

# Uncomment these when running tests
# from fastapi import FastAPI
# app = FastAPI()

# GET methods
@app.get("/", status_code=HTTP_200_OK)
def read_root():
    return {"Hello": "Bachelors"}


@app.get("/danger_zones/", status_code=HTTP_200_OK)
async def get_danger_zones():
    danger_zones = []
    results = get_danger_zones_documents()

    for result in results:
        result_id = str(result.pop("_id"))
        result["_id"] = result_id
        danger_zones.append(result)

    if len(danger_zones) > 0:
        return {"message": HTTP_200_OK, "danger_zones": danger_zones}
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No danger zones found"
        )


# ONLY FOR TESTING
# @app.get("/send_notification/", status_code=HTTP_200_OK)
# async def send_notification():
#     response = send_push_message(
#         token="ExponentPushToken[bhz8GWJ9N98LtKk_fN3My1]",
#         message="TESTING NOTIFICATION PUSHING",
#     )
#     print(response)
#     return True


# POST methods
@app.post("/create_alert/", status_code=HTTP_201_CREATED)
async def create_alert(button_event: ButtonPressEvent):
    # 1) parse/validate JSON
    button_event.location = dict(button_event.location)
    button_event = dict(button_event)

    print(button_event)

    # 2) Create event in DB
    result = post_document(document=button_event, collection_name="events")
    print(result)
    button_event["_id"] = str(result.inserted_id)

    # TODO: 3) get list of nearby responder IDs
    responders: list = get_responders_within_range_from_db(
        coordinates=button_event["location"]["coordinates"],
        userID=button_event["userID"],
    )
    print(responders)

    try:
        #3.5) send alerts to nearby responders
        for responder in responders:  # type: LatestLocation
            print(responder)
            message = send_push_message(
                token=responder["expo_token"],
                message="There's an emergency!",
                data=button_event,
            )
    except KeyError:
        if len(responders) < 1:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="No responders found within 2000m range of long:{long},lat:{lat}".format(
                    long=button_event.location.coordinates[0],
                    lat=button_event.location.coordinates[1],
                ),
            )

    # update user's latest location with the one from button_event
    # update event status to "message_sent"
    # result = update_document(....)

    if result.acknowledged == True and message == True:
        return {
            "response": HTTP_201_CREATED,
            "message": "alert created",
        }
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="event creation failed"
        )


@app.post("/nearest_responder/", status_code=status.HTTP_200_OK)
async def get_nearest_responder(location: LatestLocation):
    nearest_responder = get_nearest_responder_from_db(
        coordinates=location.location.coordinates, userID=location.userID
    )
    if nearest_responder is not None:
        return {"message": HTTP_200_OK, "nearest_responder": nearest_responder}
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No responder within range"
        )


@app.post("/responders_within_range/", status_code=status.HTTP_200_OK)
async def get_nearest_responders(location: LatestLocation, distance: int = 2000):
    nearest_responders = get_responders_within_range_from_db(
        coordinates=location.location.coordinates,
        userID=location.userID,
        distance=distance,
    )
    if nearest_responders is not None:
        return {"message": HTTP_200_OK, "nearest_responder": nearest_responders}
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No responder within range"
        )


# PUT methods
@app.put("/update_location/", status_code=HTTP_201_CREATED)
async def log_user_location(user_location: LatestLocation):
    user_location.location = dict(user_location.location)
    user_location = dict(user_location)
    response = update_location(document=user_location, collection_name="locations")
    if response.acknowledged:
        return {"message": HTTP_201_CREATED}
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="location update failed"
        )


# _id must be provided
@app.put("/accept_alert/", status_code=HTTP_200_OK)
async def accept_alert(button_event: ButtonPressEvent, _id: str):

    # 1) parse/validate JSON
    if button_event.responderID == "" or (len(button_event.responderID) < 1):
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="responderID is missing. Check your payload.",
        )
    # Add the _id from path param into the object

    # Change the location object to dict
    button_event.location = dict(button_event.location)
    button_event = dict(button_event)
    button_event["_id"] = _id
    # 2) update DB
    accept_result = accept_event_in_db(button_event)
    if accept_result.modified_count == 1:

        # Notify ROH
        send_push_message(
            token=get_expo_token(button_event["userID"], False),
            message="Request for help accepted by responder",
            data={},  # Not quite sure what we might want here
        )
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="Database update unsucesful."
        )

    return {"status": HTTP_200_OK, "message": "Response accepted and ROH notified"}


# Comment this when running tests
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
