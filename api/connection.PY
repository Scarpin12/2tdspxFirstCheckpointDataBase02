import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

def obter_conexao():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    try:
        conn = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        return conn
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"Erro ao conectar: {error_obj.message}")
        return None