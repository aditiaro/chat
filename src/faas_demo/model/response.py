from pydantic import BaseModel

class ChatResponseModel(BaseModel):
    message: str
    sender: str
    