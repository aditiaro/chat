from fastapi import FastAPI
from fastapi import Request
import logging
from model import models
from model.database import engine
from app import router
import uvicorn

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG or the desired level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Log information about the application startup
logger.info("Application starting up...")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(router)

# Middleware for logging incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    # Log information about starting the server
    logger.info("Starting the server...")
    
    # Run the application using uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8888)
