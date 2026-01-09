from sqlalchemy.orm import Session

from app.repositories import node_repo
from app.repositories import edge_repo

from app.schemas.graph import GraphResponse
from app.schemas.node import NodeResponse, NodeCreate, NodeDeleteRequest
from app.schemas.edge import EdgeResponse, EdgeCreate, EdgeDeleteRequest, EdgeSwapRequest
from app.core.exceptions import NodeNotFoundError, EdgeNotFoundError


def get_graph(db: Session) -> GraphResponse:
    nodes = node_repo.get_all_nodes(db)
    edges = edge_repo.get_all_edges(db)

    return GraphResponse(nodes=[NodeResponse(id=node.id) for node in nodes],
                         edges=[EdgeResponse(id=edge.id,
                                             from_node_id=edge.from_node_id,
                                             to_node_id=edge.to_node_id) for edge in edges])

def clear_graph(db: Session) -> None:
    node_repo.delete_all_nodes(db)

###

def create_nodes(db: Session, nodes: list[NodeCreate]) -> list[NodeResponse]:
    db_nodes = node_repo.create_nodes(db, count=len(nodes))

    return [NodeResponse(id=node.id) for node in db_nodes]

def get_reachable_nodes(db: Session, node_id: int) -> list[NodeResponse]:
    node = node_repo.get_node(db, node_id)

    if not node:
        raise NodeNotFoundError(f'Node with ID: {node_id} not found.')

    reachable_nodes = node_repo.get_reachable_nodes(db, node_id)

    return [NodeResponse(id=node.id) for node in reachable_nodes]

def delete_nodes(db, nodes: NodeDeleteRequest) -> None:
    node_ids = {node_id for node_id in nodes.node_ids}
    existing_nodes = node_repo.get_nodes(db, nodes.node_ids)

    result_ids = {node.id for node in existing_nodes}
    difference = list(result_ids ^ node_ids)

    if len(difference) != 0:
        raise NodeNotFoundError(f'Node(s) with ID(s): {difference} not found.')

    node_repo.delete_nodes(db, nodes.node_ids)

###

def create_edges(db: Session, edges: list[EdgeCreate]) -> list[EdgeResponse]:
    node_ids = {edge.from_node_id for edge in edges} | {edge.to_node_id for edge in edges}
    existing_nodes = node_repo.get_nodes(db, list(node_ids))

    result_ids = {node.id for node in existing_nodes}
    difference = list(result_ids ^ node_ids)

    if len(difference) != 0:
        raise NodeNotFoundError(f'Node(s) with ID(s): {difference} not found.')

    edge_data = [(edge.from_node_id, edge.to_node_id)for edge in edges]
    created_edges = edge_repo.create_edges(db, edge_data)

    return [EdgeResponse(id=edge.id,
                         from_node_id=edge.from_node_id,
                         to_node_id=edge.to_node_id) for edge in created_edges]

def swap_edge_direction(db: Session, edge: EdgeSwapRequest) -> EdgeResponse:
    existing_edge = edge_repo.get_edge(db, edge.edge_id)

    if not existing_edge:
        raise EdgeNotFoundError(f'Edge with ID: {edge.edge_id} not found.')

    swapped_edge = edge_repo.swap_edge_direction(db, existing_edge)

    return EdgeResponse(id=swapped_edge.id,
                        from_node_id=swapped_edge.from_node_id,
                        to_node_id=swapped_edge.to_node_id)

def delete_edges(db: Session, edges: EdgeDeleteRequest) -> None:
    edge_ids = {edge_id for edge_id in edges.edge_ids}
    existing_edges = edge_repo.get_edges(db, edges.edge_ids)

    result_ids = {edge.id for edge in existing_edges}
    difference = list(result_ids ^ edge_ids)

    if len(difference) != 0:
        raise EdgeNotFoundError(f'Edge(s) with ID(s): {difference} not found.')

    edge_repo.delete_edges(db, edges.edge_ids)
