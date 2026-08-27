from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)


Base.metadata.create_all(bind=engine)
