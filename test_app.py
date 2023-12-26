import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.database import Base
from main import app

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Override the dependency to use the in-memory database
app.dependency_overrides[get_db] = TestingSessionLocal

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def tearDown(self):
        # Clean up any data created during tests
        db = TestingSessionLocal()
        db.query(models.User).delete()
        db.commit()

    def test_register(self):
        # Test user registration
        response = self.client.post("/register/", json={"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "testuser")
        self.assertTrue("id" in data)

    def test_login(self):
        # Test user login and token retrieval
        # First, register a test user
        self.client.post("/register/", json={"username": "testuser", "password": "testpassword"})

        # Then, attempt to login
        response = self.client.post("/token/", data={"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("access_token" in data)
        self.assertEqual(data["token_type"], "bearer")

    def test_read_conversation(self):
        # Test reading conversation
        # First, register a test user
        self.client.post("/register/", json={"username": "testuser", "password": "testpassword"})

        # Then, login to get the access token
        response = self.client.post("/token/", data={"username": "testuser", "password": "testpassword"})
        data = response.json()
        access_token = data["access_token"]

        # Use the access token to make a conversation request
        response = self.client.post("/conversation/", json={"query": "Tell me about insurance"}, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("response" in data)

if __name__ == "__main__":
    unittest.main()
