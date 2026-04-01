from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, create_schema

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Skapa databas-schema
create_schema()

temp_rooms = [
    {"number": "1",  "floor": "1", "beds": 1}, 
    {"number": "2",  "floor": "1", "beds": 2}, 
    {"number": "40", "floor": "3", "beds": 2}
]

@app.get("/")
def read_root():
    # testa databasen
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 'hello' as msg,
            version() as version
        """)
        db_status = cur.fetchone()
    return { "msg": "Välkommen till hotellets boknings-API" , "db": db_status}

@app.get("/rooms")
def rooms():
    return temp_rooms

@app.post("/bookings")
def create_bookings():
    return { "msg": "Bokningen skapades" }