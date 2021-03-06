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


class Status(str, Enum):
    received = "received"
    message_sent = "message_sent"
    message_error = "message_error"
    accepted = "accepted"
    resolved = "resolved"

    class Config:
        use_enum_values = True


class Location(BaseModel):
    type: str
    coordinates: conlist(float, min_items=2, max_items=2)  # longitude, lattitude


class LatestLocation(BaseModel):
    userID: str
    location: Location
    last_updated: datetime  # or whatever is compatible with Mongo
    country: str
    expo_token: str


class ButtonPressEvent(BaseModel):
    location: Location
    last_updated: datetime
    country: str
    userID: str
    responderID: str
    resolved: bool
    status: Status
