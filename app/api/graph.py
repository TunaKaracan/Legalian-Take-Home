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

@router.delete('/graph', status_code=status.HTTP_204_NO_CONTENT)
async def delete_graph(db: Session = Depends(get_db)):
	graph_service.clear_graph(db)

###

@router.get('/nodes/{node_id}/connected', response_model=list[NodeResponse])
async def get_connected(node_id: int, db: Session = Depends(get_db)):
	return graph_service.get_reachable_nodes(db, node_id)

@router.post('/nodes', response_model=list[NodeResponse])
async def create_nodes(nodes: list[NodeCreate] = Body(..., min_length=1), db: Session = Depends(get_db)):
	return graph_service.create_nodes(db, nodes)

@router.delete('/nodes', status_code=status.HTTP_204_NO_CONTENT)
async def delete_nodes(nodes: NodeDeleteRequest, db: Session = Depends(get_db)):
	graph_service.delete_nodes(db, nodes)

###

@router.post('/edges', response_model=list[EdgeResponse])
async def create_edges(edges: list[EdgeCreate] = Body(..., min_length=1), db: Session = Depends(get_db)):
	return graph_service.create_edges(db, edges)

@router.put('/edges', response_model=EdgeResponse)
async def swap_edge_direction(edge: EdgeSwapRequest, db: Session = Depends(get_db)):
	return graph_service.swap_edge_direction(db, edge)

@router.delete('/edges', status_code=status.HTTP_204_NO_CONTENT)
async def delete_edges(edges: EdgeDeleteRequest, db: Session = Depends(get_db)):
	graph_service.delete_edges(db, edges)
