import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from model.database import engine
from app import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # creating db and tables
app.include_router(router)

# Wrap the FastAPI app with WSGI middleware for Azure Functions compatibility
azure_function_app = WSGIMiddleware(app)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    # Handle Azure Function request using the FastAPI app
    return azure_function_app(req.environ, context.log)

# For local testing
if __name__ == "__main__":
    from fastapi import Depends
    from fastapi.security import OAuth2PasswordBearer

    # Example OAuth2 authentication dependency
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def get_current_user(token: str = Depends(oauth2_scheme)):
        # Example authentication logic, replace with your actual logic
        return {"token": token}

    # Example route with authentication dependency
    @app.get("/users/me", response_model=dict)
    async def read_users_me(current_user: dict = Depends(get_current_user)):
        return current_user
