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

def get_user(identifier: str) -> bool:
    with psycopg.connect(connection_params, autocommit=True) as connection:
        with connection.cursor() as cursor:
            if "@" in identifier:
                cursor.execute('SELECT EXISTS (SELECT 1 FROM users WHERE email = %(identifier)s);', {"identifier": identifier.lower()})
                return cursor.fetchone()[0]
            else:
                cursor.execute('SELECT EXISTS (SELECT 1 FROM users WHERE username = %(identifier)s);', {"identifier": identifier})
                return cursor.fetchone()[0]

def generate_pass_hash(password_string: str) -> str :
    password = password_string.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt).decode("utf-8")

def generate_user(user_info) -> bool:
    with psycopg.connect(connection_params, autocommit=True) as connection:
        with connection.cursor() as cursor:
            encoded_email: str = user_info.email
            user: dict = {
                    "username": user_info.username,
                    "email": encoded_email.lower(),
                    "password_hash":  generate_pass_hash(user_info.password)
            }
            cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (%(username)s, %(email)s, %(password_hash)s);', user)
            return True
