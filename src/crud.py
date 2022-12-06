from datetime import  datetime, timedelta, date
from sqlalchemy.orm import Session

from src import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create new use
    """

    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email = user.email, user_name = user.user_name, passport = user.passport, address = user.address, phone = user.phone, hashed_password = fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_account(db: Session, account: schemas.AccountCreate, user_id: int, depo_id: int):
    """
    create new accounts
    """
    depo = db.query(models.Deposit).filter(models.Deposit.id == depo_id).one()
    date_open = datetime.now()
    date_close = date_open + timedelta(days=depo.shelf_life*30)
    db_accout = models.Account(**account.dict(), date_open=date_open, date_close=date_close)
    db.add(db_accout)
    db.commit()
    db.refresh(db_accout)
    return db_accout

def create_dep(db: Session, deposit: schemas.DepositCreate):
    
    db_deposit = models.Deposit(deposit_name = deposit.deposit_name, shelf_life = deposit.shelf_life, bet = deposit.bet)
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit

def get_user(db: Session, user_id: int):
    """
    получить пользователя по его id
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    получить пользователя по его email
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_phone(db: Session, phone: int):
    """
    получить пользователя по его email
    """
    return db.query(models.User).filter(models.User.phone == phone).first()
    
def get_user_by_passport(db: Session, passport: int):

    return db.query(models.User).filter(models.User.passport == passport).first()
    
def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    
    return db.query(models.Account).offset(skip).limit(limit).all()

def read_accounts_by_user_id(db: Session, user_id: int):
    
    return db.query(models.Account).filter(models.Account.owner_acc_id == user_id).all()
    #return db.query(models.Account).filter(models.User.id == user_id).filter(models.Account.owner_acc_id == models.User.id).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()

def get_deposits(db: Session, skip: int = 0, limit: int =100):

    return db.query(models.Deposit).offset(skip).limit(limit).all()

def get_deposit_by_name(db: Session, deposit_name: str):

    return db.query(models.Deposit).filter(models.Deposit.deposit_name == deposit_name).first()

def get_deposit(db: Session, dep_id: int):

    return db.query(models.Deposit).filter(dep_id == models.Deposit.id).first()