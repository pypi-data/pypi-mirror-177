import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ["K_DATABASE"])
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
