import unittest
from fastapi.testclient import TestClient
from jose import JWTError, jwt
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

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def tearDown(self):
        # Clean up any data created during tests
        db = TestingSessionLocal()
        db.query(models.User).delete()
        db.commit()

    def test_get_user(self):
        # Test get_user function
        db = TestingSessionLocal()
        # Add a test user to the database
        test_user = models.User(username="testuser", hashed_password="testpassword")
        db.add(test_user)
        db.commit()

        # Check if the user is retrieved correctly
        user = get_user(db, username="testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_get_current_user_valid_token(self):
        # Test get_current_user with a valid token
        db = TestingSessionLocal()
        # Add a test user to the database
        test_user = models.User(username="testuser", hashed_password="testpassword")
        db.add(test_user)
        db.commit()

        # Create a valid token for the test user
        valid_token = jwt.encode({"sub": "testuser"}, security.SECRET_KEY, algorithm=security.ALGORITHM)

        # Check if the c
