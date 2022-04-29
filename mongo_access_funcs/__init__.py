import sys
from typing import List, Union
from pydantic import conlist
import pymongo
import os
from pymongo.collection import Collection

from payload_definitions import EventType, LatestLocation

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


# TODO: maybe add some validation?
def post_document(
    document: Union[dict, EventType, LatestLocation], collection_name: str
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
                "country": document["country"]
            }
        },
        upsert=True,
    )


# TODO: add the other fields
def update_event(document: Union[dict, LatestLocation], collection_name: str):
    return get_collection(collection_name=collection_name).update_one(
        filter={"userID": document["userID"]},
        update={"$set": {"location": document["location"]}},
        upsert=True,
    )


def get_document_by_ID(documentID: str, collection: Collection = get_collection()):
    return collection.find_one({"_id": "{documentID}".format(documentID)})


def get_danger_zones_documents(
    collection: Collection = get_collection(collection_name="dangerZones"),
):
    return collection.find()


def get_documents_within_range(
    coordinates: conlist(float, min_items=2, max_items=2),
    radius: float,
    collection: Collection = get_collection(),
):
    collection.find({})
    return True


# Need to figure out user/requests data models before implementing this.
# TODO: this would depend on other stuff.
# For the time being this is harcoded for bpr-tester -> events
# def get_event(event_ID: str):
#     collection = get_collection(BPR_BACKEND, EVENT_COLLECTION)
#     collection.find_one({})
#     return True


# TODO: To be implemented
# def get_closest_responders(location: list):
#     return True
