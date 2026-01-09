from typing_extensions import Sequence

from sqlalchemy import text, select, delete
from sqlalchemy.orm import Session

from app.models.node import Node


def get_node(db: Session, node_id: int) -> Node | None:
    return db.scalars(select(Node).where(Node.id == node_id)).first()

def get_nodes(db: Session, node_ids: list[int]) -> Sequence[Node]:
    return db.scalars(select(Node).where(Node.id.in_(node_ids))).all()

def get_all_nodes(db: Session) -> Sequence[Node]:
    return db.scalars(select(Node)).all()

def get_reachable_nodes(db: Session, start_node_id: int) -> Sequence[Node]:
    reachable_cte = text("""
        WITH RECURSIVE reachable AS (
            SELECT id
            FROM nodes
            WHERE id = :start_node_id
            
            UNION
            
            SELECT e.to_node_id
            FROM edges e
            JOIN reachable r ON e.from_node_id = r.id
    )
    SELECT id
    FROM reachable;
    """)

    result = db.scalars(select(Node).from_statement(reachable_cte), {"start_node_id": start_node_id}).all()

    return result

def create_nodes(db: Session, count: int) -> Sequence[Node]:
    db_nodes = [Node() for _ in range(count)]

    db.add_all(db_nodes)
    db.commit()

    for node in db_nodes:
        db.refresh(node)

    return db_nodes

def delete_nodes(db: Session, node_ids: list[int]) -> None:
    db.execute(delete(Node).where(Node.id.in_(node_ids)))
    db.commit()

def delete_all_nodes(db: Session) -> None:
    db.execute(delete(Node))
    db.commit()
