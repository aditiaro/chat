from typing import Annotated

from fastapi import FastAPI, Header, HTTPException


app = FastAPI()

@app.post("/get-chat", response_model=BotResponseModel)
async def create_item(message: MessageModel, x_token: Annotated[str, Header()]):
    pass
    # return item