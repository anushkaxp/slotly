

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine


from app.api.users import router as users_router

app = FastAPI(
    title="Slotly API",
    description="A concurrency-safe resource booking platform",
    version="0.1.0",
)


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "Slotly",
        "message": "Welcome to the Slotly API",
        "version": "0.1.0",
    }


@app.get("/health/live", tags=["Health"])
def liveness_check():
    return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
def readiness_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "ready", "database": "connected"}

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )



app.include_router(users_router)