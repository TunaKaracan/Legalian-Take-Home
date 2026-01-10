from sqlalchemy.orm import Session

from app.repositories import node_repo, edge_repo
from app.schemas.graph import GraphResponse
from app.schemas.node import NodeResponse
from app.schemas.edge import EdgeResponse
from app.scripts import seed_db


def get_graph(db: Session) -> GraphResponse:
	"""
	Get the current graph.
	:param db: Database session
	:return: The current graph
	"""

	nodes = node_repo.get_all_nodes(db)
	edges = edge_repo.get_all_edges(db)

	return GraphResponse(nodes=[NodeResponse(id=node.id) for node in nodes],
						 edges=[EdgeResponse(id=edge.id,
											 from_node_id=edge.from_node_id,
											 to_node_id=edge.to_node_id) for edge in edges])

def seed_graph(db: Session) -> GraphResponse:
	"""
	Set the graph to a pre-determined state.
	:param db: Database session
	:return: The new graph
	"""

	return seed_db.seed_graph(db)

def seed_graph_random(db: Session) -> GraphResponse:
	"""
	Set the graph to a random state.
	:param db: Database session
	:return: The new graph
	"""

	return seed_db.seed_graph_random(db)

def clear_graph(db: Session) -> None:
	"""
	Clears all nodes and edges from the graph.
	:param db: Database session
	:return: None
	"""

	node_repo.delete_all_nodes(db)
