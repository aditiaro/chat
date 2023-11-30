from datetime import timedelta
import openai
import azureopenai


from sqlalchemy.orm import Session
import os

from fastapi import APIRouter, Depends, HTTPException, status, Form

from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 

from model import auth, models, schemas, security
from model.database import get_db
from model.models import User
from prompt_engine.prompt import generate_context, qa_template

from dotenv import load_dotenv, find_dotenv

import os

os.environ.get("OPENAI_API_TYPE")
os.environ.get("OPENAI_API_VERSION")
os.environ.get("OPENAI_API_BASE")
os.environ.get("OPENAI_API_KEY")

print(os.environ["OPENAI_API_KEY"])

load_dotenv(find_dotenv())
#openai_api_key = os.environ.get("OPENAI_API_KEY")

router = APIRouter()

@router.post("/register/", response_model=schemas.UserInDBBase)
async def register(user_in: schemas.UserIn, database: Session = Depends(get_db)):
    db_user = auth.get_user(database, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        **user_in.dict(exclude={"password"}), hashed_password=hashed_password
    )
    database.add(db_user)
    database.commit()
    database.refresh(db_user)

    # Return a UserInDBBase instance
    return schemas.UserInDBBase(id=db_user.id, username=db_user.username)

#endpoint 2
@router.post("/token/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db) #to extract data from form
):
    user = auth.get_user(database, username=form_data.username)
    if not user or not security.pwd_context.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#endpoint 3s
@router.post("/conversation/")
async def read_conversation(
    query: str,
    current_user: schemas.UserInDB = Depends(auth.get_current_user),
    database: Session = Depends(get_db),
):
    db_user = database.query(User).get(current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    context = generate_context(db_user)

    # llm = OpenAI(temperature=0.0, engine="gpt-3.5-turbo-16k")
    # llm = AzureOpenAI(
    # engine="",
    # model_name="", 
    # )
    llm = AzureChatOpenAI(model_name='gpt-35-turbo-16k', deployment_name='gpt35turbo16kdep2', openai_api_version="2023-07-01-preview", openai_api_base='https://openaitrials.openai.azure.com/', openai_api_type="azure", openai_api_key='f7e330db85eb4ca5855620ca2656871e')

    prompt = PromptTemplate(
        input_variables=["context", "question"], template=qa_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    #response = chain.run(context=context, question=query)
    response = chain.run(context=context, question=query)

    return {
        "conversation":"Secure conversation",
        "current_user" : current_user.username,
        "response": response,}
     


# Tell me about insurance.
#http://127.0.0.1:8889/docs#/default/