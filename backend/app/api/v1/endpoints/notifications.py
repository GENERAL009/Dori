from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db, AsyncSessionLocal
from app.api.deps import get_current_user, CurrentUser
from app.services.notification_service import NotificationService
from app.schemas.notification import (
    NotificationCreate,
    NotificationAction,
    NotificationResponse,
    NotificationListResponse,
)
from app.models.notification import NotificationStatus
from app.notifications.manager import connection_manager

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    status: Optional[NotificationStatus] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = NotificationService(db)
    return await service.get_by_user(current_user.id, status, skip, limit)


@router.get("/pending", response_model=list[NotificationResponse])
async def get_pending_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = NotificationService(db)
    notifications = await service.get_pending(current_user.id)
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.post("", response_model=NotificationResponse, status_code=201)
async def create_notification(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = NotificationService(db)
    notification = await service.create(data)
    return NotificationResponse.model_validate(notification)


@router.post("/{notification_id}/action", response_model=NotificationResponse)
async def handle_notification_action(
    notification_id: UUID,
    data: NotificationAction,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = NotificationService(db)
    notification = await service.handle_action(notification_id, data.action, current_user.id)
    return NotificationResponse.model_validate(notification)


@router.post("/{notification_id}/snooze", response_model=NotificationResponse)
async def snooze_notification(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = NotificationService(db)
    notification = await service.snooze(notification_id, current_user.id)
    return NotificationResponse.model_validate(notification)


@router.post("/{notification_id}/dismiss", response_model=NotificationResponse)
async def dismiss_notification(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    service = NotificationService(db)
    notification = await service.dismiss(notification_id, current_user.id)
    return NotificationResponse.model_validate(notification)


@router.websocket("/ws/{user_id}")
async def websocket_notifications(websocket: WebSocket, user_id: UUID):
    await connection_manager.connect(websocket, str(user_id))
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "action":
                async with AsyncSessionLocal() as db:
                    try:
                        service = NotificationService(db)
                        await service.handle_action(
                            UUID(data["notification_id"]),
                            data["action"],
                            user_id,
                        )
                        await db.commit()
                        await websocket.send_json({"type": "action_confirmed", "data": data})
                    except Exception:
                        await db.rollback()
                        await websocket.send_json({"type": "error", "message": "Action failed"})
    except WebSocketDisconnect:
        connection_manager.disconnect(str(user_id))
