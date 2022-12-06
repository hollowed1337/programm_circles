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

def test_create_user():
    response = client.post( 
        "/users/",
        json={
            "email": "pa@ugrasu.ru",
            "password": "fakepassword123", 
            "user_name": "Ксения Собчак", 
            "passport": 431245, 
            "address": "г.Москва, Москва-Сити", 
            "phone": 8805553}
        )
    
    assert response.status_code == 200, response.text
    data = response.json() 
    assert data["email"] == "pa@ugrasu.ru"

def test_create_deposit():
    response = client.post( 
        "/dep/",
        json={
            "deposit_name": "Победа",
            "shelf_life": 5, 
            "bet": 21
            }
        )

    assert response.status_code == 200, response.text
    data = response.json() 
    assert data["deposit_name"] == "Победа"



def test_create_acc():
    response = client.post( 
        "/account/",
        json={
            "owner_acc_id":1,
            "owner_dep_id":1,
            "date_open": 2022-10-30,
            "date_close": 2023-10-30,
            "amount": 2000,
            }
        )

    assert response.status_code == 200, response.text
    data = response.json() 
    assert data["id"] == 1


def test_create_acc_user_exist():
    response = client.post(
        "/account/",
        json={
            "owner_acc_id":2,
            "owner_dep_id":1,
            "date_open": 2022-10-30,
            "date_close": 2023-10-30,
            "amount": 2000,
            }
        )

    assert response.status_code == 404, response.text
    data = response.json() 
    assert data["detail"] == "Пользователя с таким кодом не существует"


def test_create_acc_deposit_exist():
    response = client.post( 
        "/account/",
        json={
            "owner_acc_id":1,
            "owner_dep_id":24,
            "date_open": 2022-10-30,
            "date_close": 2023-10-30,
            "amount": 2000,
            }
        )

    assert response.status_code == 404, response.text
    data = response.json() 
    assert data["detail"] == "Вклада с таким кодом не существует"


def test_read_accounts():
    response = client.get("/accounts/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["id"] == 1



def test_read_accounts_by_user_id():
    response = client.get("/accounts/user/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["id"] == 1



def test_read_accounts_by_not_found_user():
    response = client.get("/accounts/user/5")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"