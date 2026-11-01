import os
import bcrypt
import psycopg
from dotenv import load_dotenv

load_dotenv()
connection_params: str = f"""
    dbname=signup_signin_db
    user=postgres
    password={os.getenv('db_pass')}
    host=localhost
    port=5432
"""

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

def signin_user(user_info) -> bool:
    if verify_password(user_info.identifier, user_info.password):
        print("WOW")
    else:
        print("THIS SUCKS")