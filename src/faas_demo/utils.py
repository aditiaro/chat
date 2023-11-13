import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Model for the OpenAI API key
class OpenAIAPIKey(BaseModel):
    key: str

def enable_chat_history(func):
    def execute(request: Request, *args, **kwargs):
        # Extract the OpenAI API key from the request
        openai_api_key = request.headers.get("Authorization")
        if not openai_api_key:
            raise HTTPException(status_code=401, detail="OpenAI API key not provided in headers")

        # Your existing logic for clearing chat history
        current_page = func.__qualname__
        if "current_page" not in request.app.state:
            request.app.state["current_page"] = current_page
        if request.app.state["current_page"] != current_page:
            try:
                request.app.state.cache_resource.clear()
                del request.app.state["current_page"]
                del request.app.state["messages"]
            except:
                pass

        # Your existing logic for displaying chat history
        if "messages" not in request.app.state:
            request.app.state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        # Displaying messages in the console for demonstration
        for msg in request.app.state["messages"]:
            print(f"{msg['role']}: {msg['content']}")

        return func(request, *args, **kwargs)

    return execute

def display_msg(msg, author, app_state):
    """Method to display message in the console

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
        app_state: FastAPI application state
    """
    # Appending the message to the state
    app_state["messages"].append({"role": author, "content": msg})
    # Displaying messages in the console for demonstration
    print(f"{author}: {msg}")

def configure_openai_api_key(request: Request):
    # Extracting the OpenAI API key from the request headers
    openai_api_key = request.headers.get("Authorization")
    if not openai_api_key:
        raise HTTPException(status_code=401, detail="OpenAI API key not provided in headers")

    # Displaying the API key in the console for demonstration
    print(f"OpenAI API Key: {openai_api_key}")

    # You can store the API key in the request state or use it as needed
    request.app.state["OPENAI_API_KEY"] = openai_api_key

    return openai_api_key
