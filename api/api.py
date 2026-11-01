import psycopg.errors
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.signup import get_user, generate_user


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UsernameStr = Annotated[str, Field(pattern=r"^[a-zA-Z][a-zA-Z0-9_]{2,29}$")]
PasswordStr = Annotated[str, Field(pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\s]{8,64}$")]


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# Create Account
class SignUp(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    username: UsernameStr
    email: EmailStr
    password: PasswordStr

@app.get("/signup/users")
def check_user_exists(identifier: UsernameStr | EmailStr):
    return get_user(identifier)

@app.post("/signup/users", status_code=201)
def create_user(user_info: SignUp):
    try:
        return generate_user(user_info)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Username or email already exists.")


# Login Account
class SignIn(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    identifier: str
    password: PasswordStr
