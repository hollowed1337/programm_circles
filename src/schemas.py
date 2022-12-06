from datetime import date

from pydantic import BaseModel
from typing import Optional

class DepositBase(BaseModel):
    """
    Базовый класс для Вклада
    """
    deposit_name: str
    shelf_life: int
    bet: int

class DepositCreate(DepositBase):
    """
    Класс для создания Вклада, наследуемый от DepositBase
    """
    pass

class Deposit(DepositBase):
    """
    Класс для отображения Вклада
    """
    id: int

    class Config:
        """
        Задание настроек для возможности работать с объектами ORM
        """
        orm_mode = True

class UserBase(BaseModel):
    """
    Базовый класс для User
    """
    user_name: str
    passport: int
    address: Optional [str]
    phone: int
    email: str

class UserCreate(UserBase):
    """
    Пароль отображаться не должен, поэтому поле есть только тут
    """
    password: str

class User(UserBase):

    id: int
    

    class Config:
        orm_mode = True


class AccountBase(BaseModel):

    amount: int
    owner_acc_id: int
    owner_dep_id: int

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):

    date_open: date
    date_close: date | None=None
    id: int

    class Config:
        
        orm_mode = True