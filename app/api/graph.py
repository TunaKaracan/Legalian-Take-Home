from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session

from app.services import graph_service
from app.core.database import get_db
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest
from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapRequest
from app.schemas.graph import GraphResponse


router = APIRouter()

@router.get('/graph',
			response_model=GraphResponse,
			summary='Get the current graph')
async def get_graph(db: Session = Depends(get_db)):
	return graph_service.get_graph(db)

@router.post('/graph/seed',
			 response_model=GraphResponse,
			 status_code=status.HTTP_201_CREATED,
			 summary='Deterministically seed the graph')
async def seed_graph(db: Session = Depends(get_db)):
	return graph_service.seed_graph(db)

@router.post('/graph/seed_random',
			 response_model=GraphResponse,
			 status_code=status.HTTP_201_CREATED,
			 summary='Randomly seed the graph')
async def seed_graph(db: Session = Depends(get_db)):
	return graph_service.seed_graph(db)

@router.delete('/graph/clear',
			   status_code=status.HTTP_204_NO_CONTENT,
			   summary='Clear the nodes and edges')
async def clear_graph(db: Session = Depends(get_db)):
	graph_service.clear_graph(db)

###

@router.get('/nodes/{node_id}/connected',
			response_model=list[NodeResponse],
			responses={status.HTTP_404_NOT_FOUND: {'description': 'Node Not Found Error'}},
			summary='Get all reachable nodes from a node')
async def get_connected(node_id: int, db: Session = Depends(get_db)):
	return graph_service.get_reachable_nodes(db, node_id)

@router.post('/nodes',
			 response_model=list[NodeResponse],
			 status_code=status.HTTP_201_CREATED,
			 summary='Create a new node')
async def create_node(node: NodeCreate, db: Session = Depends(get_db)):
	return graph_service.create_nodes(db, [node])

@router.delete('/nodes',
			   status_code=status.HTTP_204_NO_CONTENT,
			   responses={status.HTTP_404_NOT_FOUND: {'description': 'Node Not Found Error'}},
			   summary='Delete a node')
async def delete_node(node: NodeDeleteRequest, db: Session = Depends(get_db)):
	graph_service.delete_nodes(db, [node])

###

@router.post('/edges',
			 response_model=list[EdgeResponse],
			 status_code=status.HTTP_201_CREATED,
			 responses={status.HTTP_404_NOT_FOUND: {'description': 'Node Not Found Error'}},
			 summary='Create a new edge between node(s)')
async def create_edge(edge: EdgeCreate, db: Session = Depends(get_db)):
	return graph_service.create_edges(db, [edge])

@router.put('/edges',
			response_model=list[EdgeResponse],
			responses={status.HTTP_404_NOT_FOUND: {'description': 'Edge Not Found Error'}},
			summary='Swap the direction of an edge')
async def swap_edge_direction(edge: EdgeSwapRequest, db: Session = Depends(get_db)):
	return graph_service.swap_edge_directions(db, [edge])

@router.delete('/edges',
			   status_code=status.HTTP_204_NO_CONTENT,
			   responses={status.HTTP_404_NOT_FOUND: {'description': 'Edge Not Found Error'}},
			   summary='Delete an edge')
async def delete_edge(edge: EdgeDeleteRequest, db: Session = Depends(get_db)):
	graph_service.delete_edges(db, [edge])
