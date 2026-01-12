from sqlalchemy.orm import Session

from app.repositories import node_repo
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest
from app.core.exceptions import NodeNotFoundError
from app.services.assertions import assert_nodes


def get_reachable_nodes(db: Session, node_id: int) -> list[NodeResponse]:
	"""
	Return all nodes reachable from the given node via directed edges.

	:raises NodeNotFoundError: If the node does not exist.
	"""

	node = node_repo.get_node(db, node_id)

	if not node:
		raise NodeNotFoundError(node_id)

	reachable_nodes = node_repo.get_reachable_nodes(db, node_id)

	return [NodeResponse(id=node.id) for node in reachable_nodes]


def create_nodes(db: Session, nodes: list[NodeCreate]) -> list[NodeResponse]:
	"""
	Create one or more new nodes and return their assigned IDs.
	"""

	created_nodes = node_repo.create_nodes(db, count=len(nodes))

	return [NodeResponse(id=node.id) for node in created_nodes]


def delete_nodes(db, nodes: list[NodeDeleteRequest]) -> None:
	"""
	Delete the specified nodes from the graph.

	:raises NodeNotFoundError: If any requested node does not exist.
	"""

	node_ids = assert_nodes(db, nodes)

	node_repo.delete_nodes(db, node_ids)
