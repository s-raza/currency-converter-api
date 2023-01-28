from typing import Any, Dict

from fastapi import APIRouter

diagnostics_router = APIRouter()


@diagnostics_router.get("/status")
async def api_status() -> Dict[str, Any]:
    return {"success": True, "status": "up"}
