from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = [{"number": "1", "floor": "1", "beds": 1}, {"number": "2", "floor": "1", "beds": 2}, {"number": "40", "floor": "3", "beds": 2}]

@app.get("/")
def read_root():
    return { "msg": "Tjenixen igen!", "v": "0.2" }

@app.get("/api/ip")
def read_root(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

@app.get("/rooms")
def read_root():
    return rooms