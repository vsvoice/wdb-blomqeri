from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
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

# datamodell för bokning
class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

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
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT * 
            FROM hotel_rooms
            ORDER BY room_number
        """)
        rooms = cur.fetchall()
    return rooms

@app.get("/rooms/{id}")
def get_room(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT * 
            FROM hotel_rooms
            WHERE id = %s
        """, [id])
        room = cur.fetchall()
    return room


@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (
            guest_id,
            room_id,
            datefrom,
            dateto
        ) VALUES (
            %s, %s, %s, %s
        ) RETURNING id
        """, [
            booking.guest_id, 
            booking.room_id,
            booking.datefrom,
            booking.dateto
        ])
        new_booking = cur.fetchone()
    return { "msg": "Bokningen skapades", "id": new_booking['id'] }

@app.get("/if/{term}")
def if_test(term: str):
    ret_str = "Default message..."
    if term == "hello" or term == "hi":
        ret_str = "Hello yourself!"
    elif term == "hej":
        ret_str = "Hej på dig"
    else:
        ret_str = f'Vad betyder "{term}"?'
    return { "msg": ret_str }
    