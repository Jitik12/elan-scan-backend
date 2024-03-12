from pydantic import BaseModel

class Person_For_Hostel(BaseModel):
    user_id: str
    room_no: str

