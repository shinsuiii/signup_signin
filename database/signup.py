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

def get_user(identifier) -> bool:
    with psycopg.connect(connection_params, autocommit=True) as connection:
        with connection.cursor() as cursor:
            column: str = "email" if "@" in identifier else "username"
            value: str = identifier.lower() if "@" in identifier else identifier
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE {column} = %(value)s);", {"value": value})
            return cursor.fetchone()[0]

def generate_pass_hash(password_string: str) -> str :
    password = password_string.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt).decode("utf-8")

def generate_user(user_info) -> bool:
    with psycopg.connect(connection_params, autocommit=True) as connection:
        with connection.cursor() as cursor:
            user: dict = {
                    "username": user_info.username,
                    "email": user_info.email.lower(),
                    "password_hash":  generate_pass_hash(user_info.password)
            }
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%(username)s, %(email)s, %(password_hash)s);", user)
            return True
