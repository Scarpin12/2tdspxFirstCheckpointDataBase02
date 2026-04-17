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
    except Exception as e:
        print(f"Erro de conexão (esperado na nuvem): {e}")
        return None 