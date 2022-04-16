from contextlib import nullcontext
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

from payload_definitions import ButtonPressEvent
from mongo_access_funcs import post_document

tags_metadata = []


@app.get("/", status_code=HTTP_200_OK)
def read_root():
    return {"Hello": "Bachelors"}


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
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="event creation failed")


@app.put("/update_alert/", status_code=HTTP_200_OK)
async def update_alert(button_event: ButtonPressEvent):
    # 1) parse/validate JSON

    # 2) update DB

    return True


# GET methods
@app.get("/location/{user_ID}", status_code=status.HTTP_200_OK)
async def get_last_known_location_by_userID(user_ID: str):
    return True


# POST methods
@app.post("/location/{user_ID}", status_code=HTTP_201_CREATED)
async def log_user_location(user_ID: str):
    document = {}


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
