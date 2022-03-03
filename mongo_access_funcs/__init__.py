import pymongo
import os
from pymongo.collection import Collection
import os 

ATLAS_CONNECTION = os.getenv("ATLAS_CONNECTION_STRING")


def get_collection(database_name: str, collection_name: str, connection_string: str=ATLAS_CONNECTION):
    client = pymongo.MongoClient(connection_string)
    database = client[database_name]
    collection = database[collection_name]
    return collection


# TODO: maybe add some validation?
def post_document(document: dict, collection: Collection):
    return collection.insert_one(document)


# TODO: this would depend on other stuff.
# Need to figure out user/requests data models before implementing this.
# For the time being this is harcoded for bpr-tester -> locations
def get_document(location_id: str):
    
    return True
