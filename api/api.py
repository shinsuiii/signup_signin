import psycopg.errors
from typing import Annotated
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from fastapi import FastAPI, Request, HTTPException, Response, Depends, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.signup import get_user, generate_user
from database.signin import signin_user, verify_jwt, ACCESS_TOKEN_AGE


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UsernameStr = Annotated[str, Field(pattern=r"^[a-zA-Z][a-zA-Z0-9_]{2,29}$")]
PasswordStr = Annotated[str, Field(pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\s]{8,64}$")]


class SignUp(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    username: UsernameStr
    email: EmailStr
    password: PasswordStr

class SignIn(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    identifier: UsernameStr | EmailStr
    password: PasswordStr

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/users/signup")
def check_user_exists(identifier: UsernameStr | EmailStr):
    return get_user(identifier)

@app.post("/users/signup", status_code=201)
def create_user(user_info: SignUp):
    try:
        return generate_user(user_info)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Username or email already exists.")


@app.post("/users/signin", status_code=200)
def login_user(user_info: SignIn, response: Response):
    try:
        token: str = signin_user(user_info)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials, please try again.")

    response.set_cookie(
        key="access_token",
        value=token,
        max_age=ACCESS_TOKEN_AGE * 60,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return {"message": "Logged in", "status_code": 200}


def get_current_user(access_token: Annotated[str | None, Cookie()] = None) -> dict | None:
    if access_token is None:
        raise HTTPException(status_code=401, detail="User not authenticated.")
    payload: dict | None = verify_jwt(access_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return payload

@app.get("/users/dashboard", status_code=200)
def dashboard(request: Request, user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists.")
    # user_info: dict = {"id": user["id"], "name": user["name"], "email": user["email"], "iat": user["iat"], "exp": user["exp"]}
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user": user}
    )