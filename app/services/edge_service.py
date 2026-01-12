from sqlalchemy.orm import Session

from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapDirectionRequest
from app.repositories import edge_repo
from app.services.assertions import assert_nodes, assert_edges


def get_edges(db: Session, edge_ids: list[int]) -> list[EdgeResponse]:
	"""
	Retrieve the specified edges from the graph using their IDs.

	:raises EdgeNotFoundError: If any requested edge does not exist.
	"""

	assert_edges(db, edge_ids, get_id_from_edge=lambda edge: edge)

	got_edges = edge_repo.get_edges(db, edge_ids)

	return [EdgeResponse(id=edge.id,
						 from_node_id=edge.from_node_id,
						 to_node_id=edge.to_node_id) for edge in got_edges]



def create_edges(db: Session, edges: list[EdgeCreate]) -> list[EdgeResponse]:
	"""
	Create directed edges between existing node(s). Self-loops and multiple connections between the same
	pair of nodes are allowed.

	:raises NodeNotFoundError: If any referenced node does not exist.
	"""

	node_ids = list({edge.from_node_id for edge in edges} | {edge.to_node_id for edge in edges})
	assert_nodes(db, node_ids, get_id_from_node=lambda node: node)

	edge_data = [(edge.from_node_id, edge.to_node_id) for edge in edges]
	created_edges = edge_repo.create_edges(db, edge_data)

	return [EdgeResponse(id=edge.id,
						 from_node_id=edge.from_node_id,
						 to_node_id=edge.to_node_id) for edge in created_edges]


def swap_edge_directions(db: Session, edges: list[EdgeSwapDirectionRequest]) -> list[EdgeResponse]:
	"""
    Reverse the direction of the specified edges (X -> Y becomes Y -> X).

    :raises EdgeNotFoundError: If any requested edge does not exist.
    """

	edge_ids = assert_edges(db, edges)

	swapped_edges = edge_repo.swap_edge_directions(db, edge_ids)

	return [EdgeResponse(id=swapped_edge.id,
						 from_node_id=swapped_edge.from_node_id,
						 to_node_id=swapped_edge.to_node_id) for swapped_edge in swapped_edges]


def delete_edges(db: Session, edges: list[EdgeDeleteRequest]) -> None:
	"""
    Delete the specified edges from the graph.

    :raises EdgeNotFoundError: If any requested edge does not exist.
    """

	edge_ids = assert_edges(db, edges)

	edge_repo.delete_edges(db, edge_ids)
