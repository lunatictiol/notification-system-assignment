from pydantic import BaseModel,Field
from typing import Optional,Dict


class DeviceRegisterRequest(BaseModel):
    fcm_token: str


class PublishMessageRequest(BaseModel):
    title: str = Field(..., example="Notification Title")
    body: str = Field(..., example="Notification body text")
    data: Optional[Dict[str, str]] = Field(default_factory=dict)
    image_url: Optional[str] = None
    action_url: Optional[str] = None