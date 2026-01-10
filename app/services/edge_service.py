from sqlalchemy.orm import Session

from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapDirectionRequest
from app.repositories import edge_repo
from app.services.assertions import assert_nodes, assert_edges


def create_edges(db: Session, edges: list[EdgeCreate]) -> list[EdgeResponse]:
	"""
	Create edges between pairs of nodes.
	:param db: Database session
	:param edges: List of edges between nodes
	:return: List of created edges
	"""

	node_ids = {edge.from_node_id for edge in edges} | {edge.to_node_id for edge in edges}
	assert_nodes(db, node_ids, get_id_from_node=lambda node: node)

	edge_data = [(edge.from_node_id, edge.to_node_id)for edge in edges]
	created_edges = edge_repo.create_edges(db, edge_data)

	return [EdgeResponse(id=edge.id,
						 from_node_id=edge.from_node_id,
						 to_node_id=edge.to_node_id) for edge in created_edges]

def swap_edge_directions(db: Session, edges: list[EdgeSwapDirectionRequest]) -> list[EdgeResponse]:
	"""
	Swap the direction of edges. I.e X->Y => Y->X
	:param db: Database session
	:param edges: List of edges
	:return: List of swapped edges
	"""

	edge_ids = assert_edges(db=db, edges=edges)

	swapped_edges = edge_repo.swap_edge_directions(db, edge_ids)

	return [EdgeResponse(id=swapped_edge.id,
						 from_node_id=swapped_edge.from_node_id,
						 to_node_id=swapped_edge.to_node_id) for swapped_edge in swapped_edges]

def delete_edges(db: Session, edges: list[EdgeDeleteRequest]) -> None:
	"""
	Delete edges.
	:param db: Database session
	:param edges: List of edges
	:return: None
	"""

	edge_ids = assert_edges(db=db, edges=edges)

	edge_repo.delete_edges(db, edge_ids)