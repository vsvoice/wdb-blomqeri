import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
  return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
   with get_conn() as conn, conn.cursor() as cur:
    # Create the schema
    cur.execute("""
      -- sample parent table
      CREATE TABLE IF NOT EXISTS foo (
        id SERIAL PRIMARY KEY, -- primary key
        created_at TIMESTAMP DEFAULT now()
      );

      -- relation table (reference to foo)
      CREATE TABLE IF NOT EXISTS sub_foo (
        id SERIAL PRIMARY KEY, -- primary key
        created_at TIMESTAMP DEFAULT now(),
        foo_id INT REFERENCES foo(id),
        info VARCHAR
      );

      -- lägg till nya kolumner
      ALTER TABLE foo ADD COLUMN IF NOT EXISTS name VARCHAR;

      -- skapa hotelltabellen
      CREATE TABLE IF NOT EXISTS hotel (
        id SERIAL PRIMARY KEY, -- primary key
        number VARCHAR,
        floor VARCHAR,
        beds INT
      );
    """)