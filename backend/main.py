import logging
import subprocess
import os
from fastapi import FastAPI
from app.api.V1.router_wallet import router as wallet_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria a aplicação FastAPI
app = FastAPI(
    title="Wallet API",
    description="API para gerenciamento de carteiras digitais",
    version="1.0.0"
)

# Inclui os routers
app.include_router(wallet_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """
    Execute startup tasks
    """
    logger.info("Starting Wallet API...")
    
    # Execute automatic database migrations using Alembic
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
            logger.info("API will continue running, but database may not be ready")
            
    except Exception as e:
        logger.error(f"❌ Migration error: {e}")
        logger.info("API will continue running, but database may not be ready")
    
    logger.info("Wallet API startup completed!")

@app.get("/")
async def root():
    """Endpoint raiz da API"""
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