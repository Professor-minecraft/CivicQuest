import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models import User, UserRole
from app.auth import hash_password

# Import routers
from app.routers import (
    auth,
    projects,
    submissions,
    audits,
    leaderboard,
    notifications,
    certificates,
    admin
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("civicquest.main")

def seed_default_accounts():
    """
    Seed required demo accounts (ADMIN, AUDITOR) with bcrypt hashed passwords.
    Never stores plaintext passwords in the database.
    """
    db = SessionLocal()
    try:
        # Default Admin
        admin_user = db.query(User).filter(User.email == "admin@gg").first()
        if not admin_user:
            logger.info("Seeding default ADMIN account: admin@gg")
            admin_user = User(
                name="CivicQuest Administrator",
                email="admin@gg",
                password_hash=hash_password("admin"),
                role=UserRole.ADMIN,
                xp=0,
                level=1
            )
            db.add(admin_user)
        else:
            # Ensure role is ADMIN
            admin_user.role = UserRole.ADMIN

        # Default Auditor
        auditor_user = db.query(User).filter(User.email == "auditor@gg").first()
        if not auditor_user:
            logger.info("Seeding default AUDITOR account: auditor@gg")
            auditor_user = User(
                name="Community Auditor",
                email="auditor@gg",
                password_hash=hash_password("auditor"),
                role=UserRole.AUDITOR,
                xp=0,
                level=1
            )
            db.add(auditor_user)
        else:
            # Ensure role is AUDITOR
            auditor_user.role = UserRole.AUDITOR

        db.commit()
    except Exception as e:
        logger.error(f"Error seeding default accounts: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing CivicQuest database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Checking and seeding default accounts...")
    seed_default_accounts()
    yield
    # Shutdown
    logger.info("CivicQuest backend shutting down.")

app = FastAPI(
    title="CivicQuest API",
    description="A civic verification platform where citizens inspect publicly listed government development works, submit observations, and collaborate with authorized auditors.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static uploads directory for citizen photos
settings.resolved_upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(settings.resolved_upload_dir)), name="uploads")

# Include API routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(submissions.router)
app.include_router(audits.router)
app.include_router(leaderboard.router)
app.include_router(notifications.router)
app.include_router(certificates.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "platform": "CivicQuest Civic Verification Platform",
        "status": "online",
        "docs": "/docs",
        "map": "/map",
        "version": "1.0.0"
    }

@app.get("/map")
def get_interactive_map():
    """
    Renders the full interactive Folium Leaflet map generated from Works Completed.csv.
    Displays all 35,292 completed works across 504 parliamentary constituencies.
    """
    from fastapi.responses import HTMLResponse
    from pathlib import Path
    from app.services.map_generator import generate_interactive_map

    backend_dir = Path(__file__).resolve().parent.parent
    html_file = backend_dir / "data" / "works_map.html"
    if not html_file.exists():
        generate_interactive_map(output_html_path=html_file)

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    return HTMLResponse(content=content)
