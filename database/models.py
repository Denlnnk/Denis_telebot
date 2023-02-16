from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date, Table, ForeignKey

from database import Base


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    username = Column('Username', String(80), unique=True, nullable=True)
    first_name = Column('First Name', String(80), nullable=False)
    last_name = Column('Last Name', String(80), nullable=False)
    register_at = Column('Register at', Date)
    active = Column('Active', Boolean)

    def __init__(self, user_id: int, username: str, first_name: str,
                 last_name: str, active: bool, register_at: datetime):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.active = active
        self.register_at = register_at

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserQuery(Base):
    # TODO РАзобраться как лучше сохранять запрос юзеров использую ForeignKey
    __tablename__ = 'userquery'

    id = Column(Integer, primary_key=True)
    user_id = Column('User', ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user_query = Column('user query', String(120), nullable=False)

    def __init__(self, user_id: int, user_query: str):
        self.user_id = user_id
        self.user_query = user_query

    def __str__(self):
        return f"User {self.user_id} choose {self.user_query}"
