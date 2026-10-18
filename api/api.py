from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from database.signup import get_user, generate_user

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Create Account
class SignUp(BaseModel):
    username: str
    email: str
    password: str

@app.get("/signup/users")
def check_user_exists(identifier: str):
    return get_user(identifier)

@app.post("/signup/users")
def create_user(user_info: SignUp):
    return generate_user(user_info)