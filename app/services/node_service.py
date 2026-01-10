from sqlalchemy.orm import Session

from app.repositories import node_repo
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest
from app.core.exceptions import NodeNotFoundError
from app.services.assertions import assert_nodes


def get_reachable_nodes(db: Session, node_id: int) -> list[NodeResponse]:
	"""
	Get all reachable nodes from a node.
	:param db: Database session
	:param node_id: Starting node id
	:return: A list of reachable nodes
	"""

	node = node_repo.get_node(db, node_id)

	if not node:
		raise NodeNotFoundError(node_id)

	reachable_nodes = node_repo.get_reachable_nodes(db, node_id)

	return [NodeResponse(id=node.id) for node in reachable_nodes]

def create_nodes(db: Session, nodes: list[NodeCreate]) -> list[NodeResponse]:
	"""
	Create new nodes.
	:param db: Database session
	:param nodes: List of new nodes
	:return: List of new nodes
	"""

	created_nodes = node_repo.create_nodes(db, count=len(nodes))

	return [NodeResponse(id=node.id) for node in created_nodes]

def delete_nodes(db, nodes: list[NodeDeleteRequest]) -> None:
	"""
	Delete nodes.
	:param db: Database session
	:param nodes: List of nodes to delete
	:return: None
	"""

	node_ids = assert_nodes(db, nodes)

	node_repo.delete_nodes(db, node_ids)