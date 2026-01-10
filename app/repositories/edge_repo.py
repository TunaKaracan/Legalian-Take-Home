from typing_extensions import Sequence

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.edge import Edge


def get_edge(db: Session, edge_id: int) -> Edge | None:
	return db.scalars(select(Edge).where(Edge.id == edge_id)).first()

def get_edges(db: Session, edge_ids: list[int]) -> Sequence[Edge]:
	return db.scalars(select(Edge).where(Edge.id.in_(edge_ids))).all()

def get_all_edges(db: Session) -> Sequence[Edge]:
	return db.scalars(select(Edge)).all()

def create_edges(db: Session, edges: list[tuple[int, int]]) -> Sequence[Edge]:
	db_edges = [Edge(from_node_id=from_id, to_node_id=to_id) for from_id, to_id in edges]

	db.add_all(db_edges)
	db.commit()

	for edge in db_edges:
		db.refresh(edge)

	return db_edges

def swap_edge_directions(db: Session, edges: list[int]) -> Sequence[Edge]:
	edges = get_edges(db, edges)

	for edge in edges:
		if edge.from_node_id == edge.to_node_id:
			continue

		edge.from_node_id, edge.to_node_id = edge.to_node_id, edge.from_node_id

	db.commit()

	for edge in edges:
		db.refresh(edge)

	return edges

def delete_edges(db: Session, edge_ids: list[int]) -> None:
	db.execute(delete(Edge).where(Edge.id.in_(edge_ids)))
	db.commit()
