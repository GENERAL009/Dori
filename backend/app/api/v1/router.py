from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    medications,
    infusions,
    schedules,
    logs,
    prescriptions,
    notifications,
    statistics,
    dashboard,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(medications.router)
api_router.include_router(infusions.router)
api_router.include_router(schedules.router)
api_router.include_router(logs.router)
api_router.include_router(prescriptions.router)
api_router.include_router(notifications.router)
api_router.include_router(statistics.router)
api_router.include_router(dashboard.router)
