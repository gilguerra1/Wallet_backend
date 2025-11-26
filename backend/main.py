import logging
import subprocess
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.V1.router_wallet import router as wallet_router
from app.api.V1.router_deposit_withdrawal import (
    router as deposit_withdrawal_router
)
from app.api.V1.router_conversion import router as conversion_router
from app.api.V1.router_transfer import router as transfer_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Wallet API",
    description="API para gerenciamento de carteiras digitais",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wallet_router, prefix="/api/v1")
app.include_router(deposit_withdrawal_router, prefix="/api/v1")
app.include_router(conversion_router, prefix="/api/v1")
app.include_router(transfer_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """
    Executa tarefas de inicialização
    """
    logger.info("Starting Wallet API...")

    try:
        logger.info("Running Alembic database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logger.info("✅ Database migrations completed successfully!")
        else:
            logger.error(f"❌ Migration failed: {result.stderr}")
            logger.info(
                "API will continue running, but database may not be ready")

    except Exception as e:
        logger.error(f"❌ Migration error: {e}")
        logger.info("API will continue running, but database may not be ready")

    logger.info("Wallet API startup completed!")


@app.get("/")
async def root():
    return {
        "message": "Wallet API está funcionando!",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
