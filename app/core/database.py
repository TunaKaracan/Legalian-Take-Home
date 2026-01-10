from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text

from app.core.config import settings


def create_tables():
	db = SessionLocal()
	with open('app/ddl/init.sql') as f:
		for command in f.read().split(';'):
			db.execute(text(command))
	db.close()

def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
create_tables()
