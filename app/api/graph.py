from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session

from app.services import graph_service
from app.core.database import get_db
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest
from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapRequest
from app.schemas.graph import GraphResponse


router = APIRouter()

@router.get('/graph', response_model=GraphResponse)
async def get_graph(db: Session = Depends(get_db)):
	return graph_service.get_graph(db)

@router.post('/graph/seed', response_model=GraphResponse)
async def seed_graph(db: Session = Depends(get_db)):
	return graph_service.seed_graph(db)

@router.delete('/graph', status_code=status.HTTP_204_NO_CONTENT)
async def clear_graph(db: Session = Depends(get_db)):
	graph_service.clear_graph(db)

###

@router.get('/nodes/{node_id}/connected', response_model=list[NodeResponse])
async def get_connected(node_id: int, db: Session = Depends(get_db)):
	return graph_service.get_reachable_nodes(db, node_id)

@router.post('/nodes', response_model=list[NodeResponse])
async def create_node(node: NodeCreate, db: Session = Depends(get_db)):
	return graph_service.create_nodes(db, [node])

@router.delete('/nodes', status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(node: NodeDeleteRequest, db: Session = Depends(get_db)):
	graph_service.delete_nodes(db, [node])

###

@router.post('/edges', response_model=list[EdgeResponse])
async def create_edge(edge: EdgeCreate, db: Session = Depends(get_db)):
	return graph_service.create_edges(db, [edge])

@router.put('/edges', response_model=list[EdgeResponse])
async def swap_edge_direction(edge: EdgeSwapRequest, db: Session = Depends(get_db)):
	return graph_service.swap_edge_directions(db, [edge])

@router.delete('/edges', status_code=status.HTTP_204_NO_CONTENT)
async def delete_edge(edge: EdgeDeleteRequest, db: Session = Depends(get_db)):
	graph_service.delete_edges(db, [edge])
