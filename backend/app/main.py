from fastapi import FastAPI
from app.routes import device
from app.db import engine, Base
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(device.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}