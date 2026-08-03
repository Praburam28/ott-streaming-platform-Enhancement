from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings
from app.db.database import engine
from app.db.base import Base

# Routers
from app.api.auth import router as auth_router
from app.api.subscription import router as subscription_router
from app.api.api_key import router as api_key_router
from app.api.content import router as content_router
from app.api.streaming import router as streaming_router
from app.api.profile import router as profile_router
from app.api.admin import router as admin_router
from app.api.reports import router as reports_router
from app.scheduler.report_scheduler import start_scheduler
from app.api.payment import router as payment_router


from app.middleware.security_headers import SecurityHeadersMiddleware
from app.models.admin.admin_audit_log import AdminAuditLog
from app.models.admin.subscription_adjustment import SubscriptionAdjustment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

start_scheduler()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/thumbnails",
    StaticFiles(directory=BASE_DIR / "uploads" / "thumbnails"),
    name="thumbnails",
)

# -----------------------------
# Middleware (FIRST)
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Content-Range",
        "Accept-Ranges",
        "Content-Length",
    ],
)

app.add_middleware(SecurityHeadersMiddleware)

# -----------------------------
# Routers (AFTER middleware)
# -----------------------------

app.include_router(auth_router)
app.include_router(subscription_router)
app.include_router(api_key_router)
app.include_router(content_router)
app.include_router(streaming_router)
app.include_router(profile_router)
app.include_router(admin_router)
app.include_router(reports_router)
app.include_router(payment_router)

# -----------------------------
# Root APIs
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "OTT Streaming Platform API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }