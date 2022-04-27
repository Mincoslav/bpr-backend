import azure.functions as func
from api_app import app
from azure.functions import AsgiMiddleware
from fastapi import HTTPException, status
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from payload_definitions import ButtonPressEvent, LatestLocation, Location
from mongo_access_funcs import (
    get_danger_zones_documents,
    post_document,
    update_location,
)


tags_metadata = []


# GET methods
@app.get("/", status_code=HTTP_200_OK)
def read_root():
    return {"Hello": "Bachelors"}


@app.get("/nearest_responders/", status_code=status.HTTP_200_OK)
async def get_nearest_responders(location: Location):
    return True


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



# POST methods
@app.post("/create_alert/", status_code=HTTP_201_CREATED)
async def create_alert(button_event: ButtonPressEvent):
    # 1) parse/validate JSON
    button_event.location = dict(button_event.location)
    button_event = dict(button_event)

    # 2) Create event in DB
    result = post_document(button_event)

    # TODO: 3) get list of nearby responder IDs

    # TODO: 3.5) send alerts to nearby responders

    if result.acknowledged == True:
        return {
            "response": HTTP_201_CREATED,
            "message": "location updated",
        }
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="event creation failed"
        )



# PUT methods
@app.put("/update_location/", status_code=HTTP_201_CREATED)
async def log_user_location(user_location: LatestLocation):
    response = update_location(document={"location":dict(user_location.location), "userID":user_location.userID}, collection_name="locations")
    if response.acknowledged:
        return {"message":HTTP_201_CREATED}
    else: raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="location update failed"
        )


@app.put("/update_alert/", status_code=HTTP_200_OK)
async def update_alert(button_event: ButtonPressEvent):
    # 1) parse/validate JSON

    # 2) update DB

    return True



def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
