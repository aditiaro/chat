import pytest
from httpx import AsyncClient

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import models
from model.database import Base

from main import app, router


DATABASE_URL = "sqlite:///./test.db"


app.dependency_overrides[get_db].__annotations__["db"] = sessionmaker(autocommit=False, autoflush=True, bind=create_engine(DATABASE_URL))


models.Base.metadata.create_all(bind=engine)

@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, World!"}

