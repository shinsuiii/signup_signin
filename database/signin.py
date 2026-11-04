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
JWT_KEY: str = os.getenv('SECRET_KEY')
ALGORITHM: str = "HS256"

def verify_password(identifier: str, plain_pass: str) -> bool:
    with psycopg.connect(connection_params, autocommit=True) as connection:
            with connection.cursor() as cursor:
                if "@" in identifier:
                    cursor.execute('SELECT password_hash FROM users WHERE email = %(identifier)s', {"identifier": identifier.lower()})
                    stored_pass: str = cursor.fetchone()[0]
                else:
                    cursor.execute('SELECT password_hash FROM users WHERE username = %(identifier)s', {"identifier": identifier})
                    stored_pass: str = cursor.fetchone()[0]
                
                if not stored_pass:
                    raise ValueError('Invalid credentials, please try again.')

                plain_bytes: bytes = plain_pass.encode("utf-8")
                hashed_bytes: bytes = stored_pass.encode("utf-8")
                return bcrypt.checkpw(plain_bytes, hashed_bytes)

def generate_jwt(identifier: str) -> str:
    with psycopg.connect(connection_params, autocommit=True) as connection:
        with connection.cursor() as cursor:
            if "@" in identifier:
                cursor.execute('SELECT * FROM users WHERE email = %(identifier)s', {"identifier": identifier.lower()})
                user_info: tuple = cursor.fetchone()
            else:
                cursor.execute('SELECT * FROM users WHERE username = %(identifier)s', {"identifier": identifier})
                user_info: tuple = cursor.fetchone()

            payload: dict = {
                "id": user_info[0],
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
                "name": user_info[1],
                "email": user_info[2],
            }

            return jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)

def signin_user(user_info) -> str | bool:
    if verify_password(user_info.identifier, user_info.password):
        return generate_jwt(user_info.identifier)
    else:
        return False

def verify_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        print("Token has expired.")
        return None
    except InvalidTokenError as error:
        print(f"Invalid token signature ({error}).")
        return None
