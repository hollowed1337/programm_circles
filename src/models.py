from sqlalchemy import  Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):

    __abstract__ =  True

    id = Column(Integer, primary_key = True, index = True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"

class User(BaseModel):
    __tablename__ = "users"
    
    user_name = Column(String, index = True)
    passport = Column(Integer, unique=True, index=True)
    address = Column(String, index=True)
    phone = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    accounts = relationship("Account", back_populates = "owner_acc")

class Account(BaseModel):
    __tablename__ = "accounts"

    owner_acc_id = Column(Integer, ForeignKey("users.id"))
    owner_dep_id = Column(Integer, ForeignKey("deposits.id"))
    date_open = Column(Date)
    date_close = Column(Date)
    amount = Column(Integer)

    owner_acc = relationship("User", back_populates="accounts")
    owner_dep = relationship("Deposit", back_populates="accounts")


class Deposit(BaseModel):
    __tablename__ = "deposits"

    deposit_name = Column(String, unique=True, index = True)
    shelf_life = Column(Integer)
    bet = Column(Integer)
    accounts = relationship("Account", back_populates = "owner_dep")

def deltatime(mouth):
    days = mouth*30
    return days