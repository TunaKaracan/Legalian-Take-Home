from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services import edge_service
from app.core.database import get_db
from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapDirectionRequest

router = APIRouter()


@router.post('',
			 response_model=list[EdgeResponse],
			 status_code=status.HTTP_201_CREATED,
			 responses={status.HTTP_404_NOT_FOUND: {'description': 'Node Not Found Error'}},
			 summary='Create a new edge between node(s)')
def create_edge(edge: EdgeCreate, db: Session = Depends(get_db)):
	return edge_service.create_edges(db, [edge])


@router.put('',
			response_model=list[EdgeResponse],
			responses={status.HTTP_404_NOT_FOUND: {'description': 'Edge Not Found Error'}},
			summary='Swap the direction of an edge')
def swap_edge_direction(edge: EdgeSwapDirectionRequest, db: Session = Depends(get_db)):
	return edge_service.swap_edge_directions(db, [edge])


@router.delete('',
			   status_code=status.HTTP_204_NO_CONTENT,
			   responses={status.HTTP_404_NOT_FOUND: {'description': 'Edge Not Found Error'}},
			   summary='Delete an edge')
def delete_edge(edge: EdgeDeleteRequest, db: Session = Depends(get_db)):
	edge_service.delete_edges(db, [edge])
