from fastapi import FastAPI
from app.routes import device
app = FastAPI()

app.include_router(device.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}