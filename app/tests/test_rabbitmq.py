from fastapi.testclient import TestClient
from app.main import app, REDIS_CONNECTION_STRING
import pika

client = TestClient(app)


def test_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('Rabbitmq'))
        if connection.is_open:
            conn = True
            connection.close()
    except:
        conn = False
    
    assert conn == True