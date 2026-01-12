from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services import node_service
from app.core.database import get_db
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest

router = APIRouter()


@router.get('/{node_id}',
			response_model=list[NodeResponse],
			responses={status.HTTP_404_NOT_FOUND: {'description': 'Node not found Error'}},
			summary='Get node using its ID')
def get_nodes(node_id: int, db: Session = Depends(get_db)):
	return node_service.get_nodes(db, [node_id])


@router.get('/{node_id}/connected',
			response_model=list[NodeResponse],
			responses={status.HTTP_404_NOT_FOUND: {'description': 'Node Not Found Error'}},
			summary='Get all reachable nodes from a node')
def get_connected(node_id: int, db: Session = Depends(get_db)):
	return node_service.get_reachable_nodes(db, node_id)


@router.post('',
			 response_model=list[NodeResponse],
			 status_code=status.HTTP_201_CREATED,
			 summary='Create a new node')
def create_node(node: NodeCreate, db: Session = Depends(get_db)):
	return node_service.create_nodes(db, [node])


@router.delete('',
			   status_code=status.HTTP_204_NO_CONTENT,
			   responses={status.HTTP_404_NOT_FOUND: {'description': 'Node Not Found Error'}},
			   summary='Delete a node')
def delete_node(node: NodeDeleteRequest, db: Session = Depends(get_db)):
	node_service.delete_nodes(db, [node])
