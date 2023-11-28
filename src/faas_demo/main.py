from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from model import models
from model.database import engine
from app import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #creating db and tables

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8889) #running on local host

