from typing import Union
import pymongo
import os
from pymongo.collection import Collection
import os

from payload_definitions import EventType 

ATLAS_CONNECTION = os.getenv("ATLAS_CONNECTION_STRING")
DATABASE_NAME = "bpr-backend"
EVENT_COLLECTION = "events"


def get_collection(database_name: str, collection_name: str, connection_string: str=ATLAS_CONNECTION):
    client = pymongo.MongoClient(connection_string)
    database = client[database_name]
    collection = database[collection_name]
    return collection


# TODO: maybe add some validation?
def post_document(document: Union[dict, EventType], collection: Collection):
    if collection == EVENT_COLLECTION:
        document is EventType
    return collection.insert_one(document)


def get_document_by_ID(documentID: str, collection: Collection):
    return collection.find_one({"_id": "{documentID}".format(documentID=documentID)})



# TODO: this would depend on other stuff.
# Need to figure out user/requests data models before implementing this.
# For the time being this is harcoded for bpr-tester -> events
# def get_event(event_ID: str):
#     collection = get_collection(DATABASE_NAME, EVENT_COLLECTION)
#     collection.find_one({})
#     return True


#TODO: To be implemented
# def get_closest_responders(location: list):
#     return True