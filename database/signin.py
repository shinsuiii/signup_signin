import jwt
import os
import bcrypt
import psycopg
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

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
            # https://www.google.com/search?q=python+jwt+encode+and+decode&oq=python+jwt+encode+and+dec&gs_lcrp=EgZjaHJvbWUqCAgBEAAYFhgeMgYIABBFGDkyCAgBEAAYFhgeMggIAhAAGBYYHjIICAMQABgWGB4yCAgEEAAYFhgeMgcIBRAAGO8FMgcIBhAAGO8FMgcIBxAAGO8F0gEINjg1M2owajeoAgCwAgA&sourceid=chrome&source=chrome.ob&ie=UTF-8

            if "@" in identifier:
                cursor.execute('SELECT * FROM users WHERE email = %(identifier)s', {"identifier": identifier.lower()})
                user_info: tuple = cursor.fetchone()
            else:
                cursor.execute('SELECT * FROM users WHERE username = %(identifier)s', {"identifier": identifier})
                user_info: tuple = cursor.fetchone()

            payload: dict = {
                "id": user_info[0],
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
                "name": user_info[1],
                "email": user_info[2],
            }

            return jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str) -> bool:

    return

def signin_user(user_info) -> bool:
    identifier: str = user_info.identifier
    password: str = user_info.password
    if verify_password(identifier, password):
        print("WOW")
    else:
        return False