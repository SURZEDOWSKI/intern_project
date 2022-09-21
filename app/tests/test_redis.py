from fastapi.testclient import TestClient
from app.main import app, REDIS_CONNECTION_STRING
import redis

client = TestClient(app)


def test_redis_connection():
    redis_client = redis.from_url(REDIS_CONNECTION_STRING)
    assert redis_client.ping() == True
        

