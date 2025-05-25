# routes/device.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.schemas import DeviceRegisterRequest
from app.models import DeviceToken
from app.dependencies import get_db

router = APIRouter(
    prefix="/devices",     
)

@router.post("/register")
async def register_device(
    payload: DeviceRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Check if token already exists
        result = await db.execute(select(DeviceToken).where(DeviceToken.fcm_token == payload.fcm_token))
        existing = result.scalar_one_or_none()

        if existing:
            return {
                "status": "already_registered",
                "token": existing.fcm_token
            }

        # Save new token
        new_token = DeviceToken(fcm_token=payload.fcm_token)
        db.add(new_token)
        await db.commit()

        return {
            "status": "registered",
            "token": new_token.fcm_token
        }

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )