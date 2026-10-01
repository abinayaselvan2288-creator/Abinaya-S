from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routes import auth, planners, history, pages


app = FastAPI(
    title="PocketSmart AI",
    description="Smart Budget & Recommendation Assistant",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(pages.router)

app.include_router(
    auth.router,
    prefix="/api"
)

app.include_router(
    planners.router,
    prefix="/api"
)

app.include_router(
    history.router,
    prefix="/api"
)


# ---------------------------------------------------------
# Startup
# ---------------------------------------------------------

@app.on_event("startup")
def startup():
    init_db()


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "PocketSmart AI"
    } 