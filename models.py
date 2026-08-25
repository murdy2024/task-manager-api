from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class TaskDB(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)