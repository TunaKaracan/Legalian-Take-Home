from typing_extensions import Callable, Iterable, TypeVar, Sequence, Set

from sqlalchemy.orm import Session

from app.repositories import node_repo, edge_repo
from app.schemas.graph import GraphResponse
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest
from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapRequest
from app.core.exceptions import NodeNotFoundError, EdgeNotFoundError
from app.scripts import seed_db


TReq = TypeVar('TReq', bound=object)
TRes = TypeVar('TRes', bound=object)
TId = TypeVar('TId', bound=int)
TExc = TypeVar('TExc', bound=Exception)

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

def clear_graph(db: Session) -> None:
    """
    Clears all nodes and edges from the graph.
    :param db: Database session
    :return: None
    """

    node_repo.delete_all_nodes(db)

###

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

    db_nodes = node_repo.create_nodes(db, count=len(nodes))

    return [NodeResponse(id=node.id) for node in db_nodes]

def delete_nodes(db, nodes: list[NodeDeleteRequest]) -> None:
    """
    Delete nodes.
    :param db: Database session
    :param nodes: List of nodes to delete
    :return: None
    """

    node_ids = assert_nodes(db, nodes)

    node_repo.delete_nodes(db, node_ids)

###

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

def swap_edge_directions(db: Session, edges: list[EdgeSwapRequest]) -> list[EdgeResponse]:
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

###

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

    return assert_resources(db=db,
                            resources=nodes,
                            get_id_from_resource=get_id_from_node,
                            fetch_existing=fetch_existing,
                            get_id_from_existing=get_id_from_existing,
                            exception_factory=node_exception)

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

    return assert_resources(db=db,
                            resources=edges,
                            get_id_from_resource=get_id_from_edge,
                            fetch_existing=fetch_existing,
                            get_id_from_existing=get_id_from_existing,
                            exception_factory=edge_exception)

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
