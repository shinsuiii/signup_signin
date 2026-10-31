from typing import Annotated
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.signup import get_user, generate_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UsernameStr = Annotated[str, Field(pattern=r"^[A-Za-z\d@$!%*?&]{3,30}$")]
PasswordStr = Annotated[str, Field(pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")]

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Create Account
class SignUp(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: PasswordStr

@app.get("/signup/users")
def check_user_exists(identifier: UsernameStr):
    return get_user(identifier)

@app.post("/signup/users")
def create_user(user_info: SignUp):
    return generate_user(user_info)