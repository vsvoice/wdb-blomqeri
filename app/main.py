from fastapi import FastAPI, Request

app = FastAPI()

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
