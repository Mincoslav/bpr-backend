import sys
from typing import List, Union
from unittest import result
from pydantic import conlist
import pymongo
import os
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor
from bson.objectid import ObjectId

from payload_definitions import ButtonPressEvent, EventType, LatestLocation

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
ATLAS_CONNECTION = os.environ["ATLAS_CONNECTION_STRING"]
BPR_BACKEND = "bpr-backend"
EVENT_COLLECTION = "events"


def get_collection(
    database_name: str = BPR_BACKEND,
    collection_name: str = EVENT_COLLECTION,
    connection_string: str = ATLAS_CONNECTION,
):
    client = pymongo.MongoClient(connection_string)
    database = client[database_name]
    collection = database[collection_name]
    return collection


def post_document(
    document: Union[dict, LatestLocation], collection_name: str
):
    return get_collection(collection_name=collection_name).insert_one(document)


def update_location(document: Union[dict, LatestLocation], collection_name: str):
    return get_collection(collection_name=collection_name).update_one(
        filter={"userID": document["userID"]},
        update={
            "$set": {
                "userID": document["userID"],
                "location": document["location"],
                "last_updated": document["last_updated"],
                "country": document["country"],
                "expo_token": document["expo_token"],
            }
        },
        upsert=True,
    )


# TODO: add the other fields
def accept_event_in_db(
    document: Union[dict, ButtonPressEvent],
    collection: Collection = get_collection(collection_name=EVENT_COLLECTION),
):
    # print(collection.database)
    # print(document["userID"])
    # result = collection.find_one({})
    # print(result)
    # for item in result:
    #     print(item)
    # return True
    return collection.update_one(
        filter={"_id": ObjectId(document["_id"])},
        update={
            "$set": {
                "location": document["location"],
                "last_updated": document["last_updated"],
                "responderID": document["responderID"],
                "status": "accepted",
            }
        },
        upsert=False,
    )


# def get_document_by_ID(documentID: str, collection: Collection = get_collection()):
#     return collection.find_one({"_id": "{documentID}".format(documentID)})


def get_danger_zones_documents(
    collection: Collection = get_collection(collection_name="dangerZones"),
):
    return collection.find()


def get_nearest_responder_from_db(
    coordinates: conlist(float, min_items=2, max_items=2),
    userID: str,
    collection: Collection = get_collection(collection_name="locations"),
):
    results = collection.aggregate(
        [
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": coordinates},
                    # "maxDistance": 2000,
                    "spherical": True,
                    "distanceField": "distance",
                }
            }
        ]
    )
    for result in results:
        # print(result)
        if result["userID"] != userID:
            result.pop("_id")
            return result
    return None


def get_responders_within_range_from_db(
    coordinates: conlist(float, min_items=2, max_items=2),
    userID: str,
    distance: int = 2000,
    collection: Collection = get_collection(collection_name="locations"),
):
    results = list(
        collection.aggregate(
            [
                {
                    "$geoNear": {
                        "near": {"type": "Point", "coordinates": coordinates},
                        "maxDistance": distance,
                        "spherical": True,
                        "distanceField": "distance",
                    }
                },
                {
                    "$group": {
                        "_id": "$expo_token",
                        "location": {"$first": "$location"},
                        "userID": {"$first": "$userID"},
                        "country": {"$first": "$country"},
                        "last_updated": {"$first": "$last_updated"},
                        "distance": {"$first": "$distance"},
                    }
                },
                {"$sort": {"distance": 1}},
            ]
        )
    )

    index = 0
    while index < len(results):

        if results[index]["userID"] == userID:
            del results[index]
            index = 0
            continue

        else:
            results[index]["_id"] = str(results[index]["_id"])
            index += 1

    if len(results) == 0:
        return None
    return results


def get_expo_token(
    ID: str,
    isResponder: bool,
    collection: Collection = get_collection(collection_name="events"),
):
    if isResponder:
        user = "responderID"
    else:
        user = "userID"

    result = collection.aggregate(
        pipeline=[
            {"$match": {user: ID}},
            {
                "$lookup": {
                    "from": "locations",
                    "localField": "userID",
                    "foreignField": "userID",
                    "as": "user_location",
                }
            },
        ]
    )
    token = list(result)[0]
    print(token)
    # ["user_location"]["expo_token"])
    return token["user_location"][0]["expo_token"]


# Need to figure out user/requests data models before implementing this.
# TODO: this would depend on other stuff.
# For the time being this is harcoded for bpr-tester -> events
# def get_event(event_ID: str):
#     collection = get_collection(BPR_BACKEND, EVENT_COLLECTION)
#     collection.find_one({})
#     return True
