from typing import Union
from pydantic import BaseModel, conlist
from datetime import datetime
from enum import Enum


# TODO: We might not even need this tbh
class EventType(Enum):
    Pregnancy = "Pregnancy"
    Crime = "Crime"
    HealthProblem = "Health Problem"
    Fire = "Fire"
    Accident = "Accident"
    Violence = "Violence"


class Status(str,Enum):
    received = "received"
    message_sent = "message_sent"
    message_error = "message_error"
    accepted = "accepted"
    resolved = "resolved"
    class Config:  
        use_enum_values = True 


class Location(BaseModel):
    location_type: str  # We might want to keep radius/point so use this to ensure schema integrity
    coordinates: conlist(float, min_items=2, max_items=2)  # lattitude, longitude
    last_updated: datetime  # or whatever is compatible with Mongo
    country: str


class ButtonPressEvent(BaseModel):
    location: Location
    userID: str
    responderID: str
    resolved: bool
    status: Status
