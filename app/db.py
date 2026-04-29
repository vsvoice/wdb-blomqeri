import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
  return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
   with get_conn() as conn, conn.cursor() as cur:
    # Create the schema
    cur.execute("""

      -- Lägg till pgcrypto
      CREATE EXTENSION IF NOT EXISTS pgcrypto;
    

      -- skapa hotelltabellen
      CREATE TABLE IF NOT EXISTS hotel (
        id SERIAL PRIMARY KEY, -- primary key
        number VARCHAR,
        floor VARCHAR,
        beds INT
      );

      -- skapa hotel_rooms-tabellen
      CREATE TABLE IF NOT EXISTS hotel_rooms (
        id SERIAL PRIMARY KEY,
        room_number INT,
        type VARCHAR,
        price NUMERIC
      );

      -- skapa hotel_guests-tabellen
      CREATE TABLE IF NOT EXISTS hotel_guests (
        id SERIAL PRIMARY KEY,
        firstname VARCHAR,
        lastname VARCHAR,
        address VARCHAR
      );
      ALTER TABLE hotel_guests ADD COLUMN IF NOT EXISTS api_key VARCHAR DEFAULT encode(gen_random_bytes(32), 'hex');

      -- skapa hotel_bookings-tabellen
      CREATE TABLE IF NOT EXISTS hotel_bookings (
        id SERIAL PRIMARY KEY,
        guest_id INT REFERENCES hotel_guests(id),
        room_id INT REFERENCES hotel_rooms(id),
        datefrom DATE,
        dateto DATE,
        addinfo VARCHAR
      );
      ALTER TABLE hotel_bookings ADD COLUMN IF NOT EXISTS stars INT;

      -- ändra kolumn efteråt 
      -- ALTER TABLE hotel_bookings ALTER COLUMN datefrom SET DEFAULT NOW();

    """)