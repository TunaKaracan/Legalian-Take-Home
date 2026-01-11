from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services import graph_service
from app.core.database import get_db
from app.schemas.graph import GraphResponse

router = APIRouter()

@router.get('/',
			response_model=GraphResponse,
			summary='Get the current graph')
def get_graph(db: Session = Depends(get_db)):
	return graph_service.get_graph(db)


@router.post('/seed',
			 response_model=GraphResponse,
			 status_code=status.HTTP_201_CREATED,
			 summary='Deterministically seed the graph')
def seed_graph(db: Session = Depends(get_db)):
	return graph_service.seed_graph(db)


@router.post('/seed_random',
			 response_model=GraphResponse,
			 status_code=status.HTTP_201_CREATED,
			 summary='Randomly seed the graph')
def seed_graph(db: Session = Depends(get_db)):
	return graph_service.seed_graph_random(db)
