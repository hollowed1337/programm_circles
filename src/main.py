from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Зависимости 
def get_db():
    """
    Задаем зависимость к БД
    При каждом запросе будет 
    создаваться новое подключение
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Создание пользователя
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    db_user_phone = crud.get_user_by_phone(db, phone=user.phone)
    db_user_passport = crud.get_user_by_passport(db, passport=user.passport)
    if db_user: 
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_phone:
        raise HTTPException(status_code=1004, detail="Номер телефона уже используется")
    if db_user_passport:
        raise HTTPException(status_code=400, detail="Номер пасспорта уже используется")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка пользователей
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получение пользователя по id
    Если такого нет - выдется ошибка"""

    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/dep/", response_model=schemas.Deposit)
def create_dep(dep: schemas.DepositCreate, db: Session = Depends(get_db)):
    """
    Создание вклада
    """
    db_depo = crud.get_deposit_by_name(db,deposit_name= dep.deposit_name)
    if db_depo: 
        raise HTTPException(status_code=201, detail="Вклад с таким наименованием уже существует")
    return crud.create_dep(db=db, deposit=dep)


@app.get("/dep/", response_model=list[schemas.Deposit])
def read_deposits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка вкладов
    """
    deposits = crud.get_deposits(db, skip=skip, limit=limit)
    return deposits


@app.post("/accounts/", response_model=schemas.Account)
def create_acc(acc: schemas.AccountCreate, owner_acc_id: int, owner_dep_id: int, db: Session = Depends(get_db)):
    """
    Создание вклада
    """
    db_acc_user = crud.get_accounts_by_user_id(db, owner_acc_id=owner_acc_id)
    db_acc_depo = crud.get_accounts_by_depo_id(db, owner_dep_id=owner_dep_id)
    if not db_acc_user:
         raise HTTPException(status_code=404, detail="Пользователя с таким кодом не существует")
    if not db_acc_depo:
        raise HTTPException(status_code=404, detail="Вклада с таким кодом не существует")
    return crud.create_account(db=db, account=acc, user_id=owner_acc_id, depo_id=owner_dep_id)

@app.get("/accounts/", response_model=list[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка счетов
    """
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return accounts


@app.get("/accounts/{user_id}", response_model=list[schemas.Account])
def read_accounts_by_user_id(owner_acc_id: int, db: Session = Depends(get_db)):
    """
    Получение списка счетов по коду клиента
    """
    accounts = crud.get_accounts_by_user_id(db, owner_acc_id=owner_acc_id)
    if accounts is None:
        raise HTTPException(status_code=404, detail="User not found")
    return accounts
