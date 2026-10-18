CREATE DATABASE signup_signin_db;
DROP DATABASE signup_sigin_db;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name ASC;
SELECT * FROM users;
DROP TABLE users;
CREATE TABLE users(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);