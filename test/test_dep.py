from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db(): # pragma: no cover
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# def test_create_deposit():
#     response = client.post( 
#         "/dep/",
#         json={
#             "deposit_name": "Победа",
#             "shelf_life": 5, 
#             "bet": 21
#             }
#         )

#     assert response.status_code == 200, response.text
#     data = response.json() 
#     assert data["deposit_name"] == "Победа"


def test_create_deposit_exist_name():
    response = client.post( 
        "/dep/",
        json={
            "deposit_name": "Победа",
            "shelf_life": 5, 
            "bet": 21
            }
        )

    assert response.status_code == 201, response.text
    data = response.json() 
    assert data["detail"] == "Вклад с таким наименованием уже существует"


def test_get_deposits():
    response = client.get("/deps/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["deposit_name"] == "Победа"

def test_read_user():
    response = client.get("/dep/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["deposit_name"] == "Победа"

def test_deposit_not_found():
    response = client.get("/dep/41")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Deposit not found"