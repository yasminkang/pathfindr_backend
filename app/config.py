import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "rm558006")
DB_PASSWORD = os.getenv("DB_PASSWORD", "230104")
DB_HOST = os.getenv("DB_HOST", "oracle.fiap.com.br")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SID = os.getenv("DB_SID", "ord")

SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))

DATABASE_URL_SID = f"{DB_USER}/{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SID}"
DATABASE_URL_SERVICE = f"{DB_USER}/{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/orcl"
DATABASE_URL_FULL = f"{DB_USER}/{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/orcl.fiap.com.br"
DATABASE_URL = DATABASE_URL_SERVICE