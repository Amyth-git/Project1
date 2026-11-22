from time import monotonic
from typing import Any
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
import structlog

from project1.config import settings
from project1.logging import configure_logging

configure_logging()
log = structlog.get_logger()
STARTED_AT = monotonic()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Sample API for automated deployment and monitoring (Project1).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env != "production" else [],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=["/metrics", "/health", "/ready"],
).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

_items: dict[str, dict[str, Any]] = {}


class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.app_env == "development" and not x_api_key:
        return
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "env": settings.app_env}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "uptime_seconds": str(int(monotonic() - STARTED_AT))}


@app.get("/info")
def info() -> dict[str, str]:
    return {"name": settings.app_name, "env": settings.app_env, "version": "1.0.0"}


@app.get("/items")
def list_items() -> list[dict[str, Any]]:
    return list(_items.values())


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemIn, _: None = Depends(require_api_key)) -> dict[str, Any]:
    item_id = str(uuid4())
    item = {"id": item_id, **payload.model_dump()}
    _items[item_id] = item
    log.info("item_created", item_id=item_id)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str, _: None = Depends(require_api_key)) -> None:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
    log.info("item_deleted", item_id=item_id)
