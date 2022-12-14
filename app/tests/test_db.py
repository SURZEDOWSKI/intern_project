from fastapi.testclient import TestClient
from app.main import app, engine
from sqlmodel import Session
import psycopg2

client = TestClient(app)


def test_db_connection():
    with Session(engine) as session:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            host="Postgres",
            password="pass",
            port="5432",
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM information_schema.tables")
        rows = cursor.fetchall()
        for table in rows:
            print(table)
        conn.close()
        assert rows != None
