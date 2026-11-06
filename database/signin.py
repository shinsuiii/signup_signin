import jwt
import os
import bcrypt
import psycopg
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

load_dotenv()
connection_params: str = f"""
    dbname=signup_signin_db
    user=postgres
    password={os.getenv('db_pass')}
    host=localhost
    port=5432
"""
ACCESS_KEY: str = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_KEY: str = os.getenv("REFRESH_TOKEN_SECRET")

ACCESS_TOKEN_AGE: int = 15 # Minutes
REFRESH_TOKEN_AGE: int = 7 # Days

ALGORITHM: str = "HS256"

def verify_password(identifier: str, plain_pass: str) -> bool:
    with psycopg.connect(connection_params, autocommit=True) as connection:
            with connection.cursor() as cursor:
                column: str = "email" if "@" in identifier else "username"
                try:
                    cursor.execute(f"SELECT password_hash FROM users WHERE {column} = %(value)s", {"value": identifier})
                    stored_pass: str = cursor.fetchone()
                except TypeError:
                    return False

                if stored_pass is None:
                    raise ValueError('Invalid credentials, please try again.')

                return bcrypt.checkpw(plain_pass.encode("utf-8"), stored_pass[0].encode("utf-8"))

def generate_jwt(identifier: str) -> str:
    with psycopg.connect(connection_params, autocommit=True) as connection:
        with connection.cursor() as cursor:
            column: str = "email" if "@" in identifier else "username"

            cursor.execute(f"SELECT * FROM users WHERE {column} = %(value)s", {"value": identifier})
            row: tuple = cursor.fetchone()
            payload: dict = {
                "id": row[0],
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_AGE),
                "name": row[1],
                "email": row[2],
            }

            return jwt.encode(payload, ACCESS_KEY, algorithm=ALGORITHM)

def signin_user(user_info) -> str:
    if not verify_password(user_info.identifier, user_info.password):
        raise ValueError("Invalid credentials, please try again.")
    return generate_jwt(user_info.identifier)

def verify_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, ACCESS_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        print("Token has expired.")
        return None
    except InvalidTokenError as error:
        print(f"Invalid token signature ({error}).")
        return None
