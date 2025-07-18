# run_test.py
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(response.status_code)
    print(response.json())

test_root()
