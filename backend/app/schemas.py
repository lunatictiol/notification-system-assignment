from pydantic import BaseModel
from typing import Optional


class DeviceRegisterRequest(BaseModel):
    fcm_token: str


class NotificationPayload(BaseModel):
    title: str
    body: str
    data: dict = {}
    image_url: Optional[str] = None
    action_url: Optional[str] = None
