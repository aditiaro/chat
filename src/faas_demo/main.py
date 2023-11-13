from fastapi import FastAPI
import uvicorn
from model import models
from model.db import engine
from app import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8001)