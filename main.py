from fastapi import FastAPI
from routes import client, room, booking

app = FastAPI()

app.include_router(client.router)
app.include_router(room.router)
app.include_router(booking.router)
