import os

PROJECT = "Tic Tac Toe"
TOKEN_TTL = 12 * 60 * 60

MIN_GAME_SIZE = 3

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
DB_NAME = os.getenv("POSTGRES_DB", "tic_tac_toe")
