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

from payload_definitions import ButtonPressEvent, EventType, LatestLocation
from mongo_access_funcs import get_collection, get_document, post_document

tags_metadata = []


@app.get("/", status_code=HTTP_200_OK)
def read_root():
    return {"Hello": "Bachelors"}
    

# TODO: get location and user data from request and store it in db
@app.put("/create_alert/", status_code=HTTP_201_CREATED)
async def create_alert(button_event: ButtonPressEvent):
    # 1) parse/validate JSON



    # 2) update DB 

    # 3) get list of nearby responder IDs

    # 3) send alerts to nearby responders

    
   

    return True


# GET methods
@app.get("/location/{user_ID}", status_code=status.HTTP_200_OK)
async def get_last_known_location_by_userID(user_ID: str):
    return True


# POST methods
@app.post("/location/{user_ID}", status_code=HTTP_201_CREATED)
async def log_user_location(user_ID: str):
    document = {}


# @app.post("/user/", status_code=HTTP_201_CREATED)
# async def create_user(user_info: User):
#     print(user_info)
#     user = {
#         "email": user_info.email,
#         "phone_number": user_info.phone_number,
#         "latest_location": {
#             "type": user_info.latest_location.type,
#             "coordinates": user_info.latest_location.coordinates,
#             "last_updated": user_info.latest_location.last_updated,
#             "country": user_info.latest_location.country
#         },
#         "user_type": {
#             "victim": user_info.user_type.victim,
#             "responder": user_info.user_type.responder
#         }
#     }
#     collection = get_collection(database_name="bpr-backend", collection_name="users")
#     result = post_document(user, collection)

#     if result.acknowledged == True:
#         return {
#             "response": HTTP_201_CREATED,
#             "message": "User created",
#         }
#     else:
#         raise HTTPException(
#             status_code=HTTP_409_CONFLICT,
#             detail="User couldn't be created"
#         )



# @app.put("/update_location/", status_code=HTTP_200_OK)
# async def latest_location(latest_location: LatestLocation):
#     latest_location = {
#         "user_uid": latest_location.user_uid,
#         "date": latest_location.date,
#         "user_type": {
#             "victim": latest_location.user_type.victim,
#             "responder": latest_location.user_type.responder,
#         },
#         "location": {
#             "type": latest_location.location.type,
#             "coordinates": latest_location.location.coordinates,
#             "last_updated": latest_location.location.last_updated,
#             "country": latest_location.location.country,
#         },
#     }

#     collection = get_collection(
#         database_name="bpr-backend", collection_name="latest_location"
#     )
#     result = post_document(latest_location, collection)

#     if result.acknowledged == True:
#         return {
#             "response": HTTP_201_CREATED,
#             "message": "location updated",
#         }
#     else:
#         raise HTTPException(status_code=HTTP_409_CONFLICT, detail="location is fucked")


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
