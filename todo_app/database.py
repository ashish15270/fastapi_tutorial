from typing import override
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(override=True)

db_url = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(db_url, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()