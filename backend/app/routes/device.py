# routes/device.py

from fastapi import APIRouter
from app.schemas import DeviceRegisterRequest  

router = APIRouter(
    prefix="/devices",     
)

@router.post("/register")
def register_device(payload: DeviceRegisterRequest):
    return {"token": payload.fcm_token, "status": "registered"}
