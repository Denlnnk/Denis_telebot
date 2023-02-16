from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

from database.models import User
from database.models import UserQuery

Base.metadata.create_all(engine)
