from pydantic import (BaseModel, conlist)
from datetime import datetime

class LatestLocation(BaseModel):
    type: str                                                # We might want to keep radius/point so use this to ensure schema integrity
    coordinates: conlist(float, min_items=2, max_items=2)    # lattitude, longitude
    last_updated: datetime                                   # or whatever is compatible with Mongo
    country: str

class UserType(BaseModel):
    victim: bool    
    responder: bool


class User(BaseModel):
    email: str
    phone_number: str
    latest_location: LatestLocation
    user_type: UserType