from fastapi import FastAPI, Depends, UploadFile, Header
from fastapi.middleware.cors import CORSMiddleware
from tasks import tasks, models

app = FastAPI()
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/in/{user_id}")
async def user_in(user_id: str):
    response = await tasks.get_in(user_id)
    return response


@app.get("/out/{user_id}")
async def user_out(user_id: str):
    response = await tasks.get_out(user_id)
    return response


@app.post("/assign_hostel_room/")
async def get_hostel_room(person: models.Person_For_Hostel):
    print(person)
    response = await tasks.issue_hostel(person.user_id, person.room_no)
    return response


@app.post('/assign_on_spot_hostel/')
async def get_onspot_hostel(person: models.Person_For_Hostel):
    response = await tasks.hostel_on_spot(person.user_id, person.room_no)
    return response

@app.get('/leaving/{user_id}')
async def user_leaving(user_id: str):
    response = await tasks.take_keys(user_id)
    return response

"""
Getting all the people in the hostel and campus
"""


@app.get('/people_in_hostel')
async def people_in_hostel():
    response = await tasks.get_all_in_hostel()
    return response


@app.get('/people_in_campus')
async def people_in_campus():
    response = await tasks.get_all_in_campus()
    return response


@app.get('/mismatch')
async def get_count():
    response = await tasks.get_mismatch()
    return response