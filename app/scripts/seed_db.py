from sqlalchemy.orm import Session

from app.repositories import node_repo, edge_repo
from app.schemas.graph import NodeResponse, EdgeResponse, GraphResponse


def seed_graph(db: Session) -> GraphResponse:
	node_repo.delete_all_nodes(db)

	total_nodes = 25
	db_nodes = node_repo.create_nodes(db, total_nodes)

	node_ids = [node.id for node in db_nodes]
	min_id = min(node_ids)

	edges_to_create = [(0, 1), (0, 2), (0, 4), (0, 5),
						(1, 3), (1, 6), (1, 7),
						(2, 4), (2, 8),
						(3, 10),
						(5, 12),
						(6, 10),
						(7, 5), (7, 13),
						(9, 3), (9, 11),
						(10, 15),
						(11, 5),
						(12, 14),
						(14, 7), (14, 8),
						(15, 9),
						(16, 13), (16, 14),
						(17, 9),
						(18, 17),
						(19, 22),
						(20, 19), (20, 23), (20, 24),
						(21, 19),
						(22, 21)]
	edges_to_create = [(a + min_id, b + min_id) for (a, b) in edges_to_create]

	created_edges = edge_repo.create_edges(db, edges_to_create)

	return GraphResponse(
		nodes=[NodeResponse(id=n.id) for n in db_nodes],
		edges=[EdgeResponse(id=edge.id,
							from_node_id=edge.from_node_id,
							to_node_id=edge.to_node_id) for edge in created_edges])

