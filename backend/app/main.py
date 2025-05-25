from fastapi import FastAPI
from app.routes import device,notification
from app.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow Nginx-served frontend (localhost:8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(device.router)
app.include_router(notification.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}