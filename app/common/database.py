import psycopg2
from psycopg2.extras import RealDictCursor
import time

from app.common.config import config


while True:
    try:
        conn = psycopg2.connect(
            host=config.get("HOST"),
            port=config.get("PORT"),
            database=config.get("DATABASE"),
            user=config.get("USER"),
            password=config.get("PASSWORD"),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print(" Conexión exitosa a PostgreSQL")
        break
    except Exception as error:
        print(" Error al conectar:", error)
        time.sleep(2)