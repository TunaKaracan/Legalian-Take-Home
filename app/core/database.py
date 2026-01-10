from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, text

from app.core.config import settings


def create_tables():
	db = SessionLocal()

	with open('app/ddl/create_nodes_table.sql') as f:
		db.execute(text(f.read()))
	with open('app/ddl/create_edges_table.sql') as f:
		db.execute(text(f.read()))

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
