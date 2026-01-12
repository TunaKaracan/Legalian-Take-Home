from typing_extensions import Callable, Iterable, TypeVar, Sequence, Set

from sqlalchemy.orm import Session

from app.repositories import node_repo, edge_repo
from app.core.exceptions import NodeNotFoundError, EdgeNotFoundError


TReq = TypeVar('TReq', bound=object)
TRes = TypeVar('TRes', bound=object)
TId = TypeVar('TId', bound=int)
TExc = TypeVar('TExc', bound=Exception)


def assert_nodes(db: Session,
				 nodes: Sequence[TReq],
				 get_id_from_node: Callable[[TReq], TId] = lambda n: n.node_id,
				 fetch_existing: Callable[[Session, list[TId]], Iterable[TRes]] = node_repo.get_nodes,
				 get_id_from_existing: Callable[[TRes], TId] = lambda n: n.id,
				 node_exception: Callable[[list[TId]], TExc] = lambda ids: NodeNotFoundError(ids)) -> list[TId]:
	"""
	Wrapper for node assertions.
	:param db: Database session
	:param nodes: Requested nodes
	:param get_id_from_node: How to get node ID from node
	:param fetch_existing: How to fetch existing nodes
	:param get_id_from_existing: How to get node ID from existing nodes
	:param node_exception: Exception raised when node is not found
	:return: List of node IDs
	"""

	return assert_resources(db, nodes, get_id_from_node, fetch_existing, get_id_from_existing, node_exception)


def assert_edges(db: Session,
				 edges: Sequence[TReq],
				 get_id_from_edge: Callable[[TReq], TId] = lambda e: e.edge_id,
				 fetch_existing: Callable[[Session, list[TId]], Iterable[TRes]] = edge_repo.get_edges,
				 get_id_from_existing: Callable[[TRes], TId] = lambda e: e.id,
				 edge_exception: Callable[[list[TId]], TExc] = lambda ids: EdgeNotFoundError(ids)) -> list[TId]:
	"""
	Wrapper for edge assertions.
	:param db: Database session
	:param edges: Requested edges
	:param get_id_from_edge: How to get edge ID from edge
	:param fetch_existing: How to fetch existing edges
	:param get_id_from_existing: How to get node ID from existing edges
	:param edge_exception: Exception raised when edge is not found
	:return: List of edge IDs
	"""

	return assert_resources(db, edges, get_id_from_edge, fetch_existing, get_id_from_existing, edge_exception)


def assert_resources(db: Session,
					 resources: Sequence[TReq],
					 get_id_from_resource: Callable[[TReq], TId],
					 fetch_existing: Callable[[Session, list[TId]], Iterable[TRes]],
					 get_id_from_existing: Callable[[TRes], TId],
					 exception_factory: Callable[[list[TId]], TExc]) -> list[TId]:
	"""
	Asserts that a resource requested exists. If any resource does not exist, raises an appropriate exception.
	:param db: Database session
	:param resources: Requested resources
	:param get_id_from_resource: How to get the ID of the resource
	:param fetch_existing: How to fetch existing resource
	:param get_id_from_existing: How to get the ID of the existing resource
	:param exception_factory: Exception to raise if resources requested does not exist
	:return: List of the ID of the requested resources
	"""

	requested_ids: Set[TId] = {get_id_from_resource(r) for r in resources}

	existing_resources = fetch_existing(db, list(requested_ids))
	existing_ids: Set[TId] = {get_id_from_existing(r) for r in existing_resources}

	missing = sorted(requested_ids - existing_ids)

	if missing:
		raise exception_factory(missing)

	return list(requested_ids)
