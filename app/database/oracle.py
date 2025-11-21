import os
from dotenv import load_dotenv
import oracledb

# Carrega variáveis do arquivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SID = os.getenv("DB_SID")

# Monta o DSN
dsn = f"{DB_HOST}:{DB_PORT}/{DB_SID}"

def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=dsn
    )