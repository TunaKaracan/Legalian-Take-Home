from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from app.models.base import Base


DATABASE_URL = 'mysql+pymysql://root:1234@localhost:3306/graph_db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
