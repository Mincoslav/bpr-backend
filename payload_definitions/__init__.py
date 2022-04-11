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


class Status(Enum):
    Received = "received"
    MessageSent = "message_sent"
    MessageError = "message_error"
    Resolved = "resolved"


class Location(BaseModel):
    type: str  # We might want to keep radius/point so use this to ensure schema integrity
    coordinates: conlist(float, min_items=2, max_items=2)  # lattitude, longitude
    last_updated: datetime  # or whatever is compatible with Mongo
    country: str


class ButtonPressEvent(BaseModel):
    event_type: EventType
    current_location: Location
    userID: str
    responderID: str
    status: Union[Status, None]
    resolved: bool
