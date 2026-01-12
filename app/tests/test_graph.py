from typing_extensions import Callable

from fastapi.testclient import TestClient

from app.main import server
from app.scripts.seed_db import NODES_TO_CREATE, EDGES_TO_CREATE

client = TestClient(server)


def get_graph():
	response = client.get('/graph')
	assert response.status_code == 200
	return response.json()


def get_graph_nodes():
	return get_graph()['nodes']


def get_graph_edges():
	return get_graph()['edges']


def _get_min_max_id(func: Callable) -> int:
	return func([node['id'] for node in get_graph_nodes()])


def get_min_id() -> int:
	return _get_min_max_id(min)


def get_max_id() -> int:
	return _get_min_max_id(max)


def seed_graph():
	response = client.post('/graph/seed')
	assert response.status_code == 201
	return response.json()


def test_clear_graph():
	response = client.delete('/graph/clear')
	assert response.status_code == 204

	assert get_graph() == {'nodes': [], 'edges': []}


def test_seed_graph():
	graph = seed_graph()

	assert len(graph['nodes']) == NODES_TO_CREATE
	assert len(graph['edges']) == len(EDGES_TO_CREATE)

	min_id = get_min_id()

	for node in graph['nodes']:
		assert min_id <= node['id'], node['id'] <= min_id + (NODES_TO_CREATE - 1)

	for edge in graph['edges']:
		assert any([(edge['from_node_id'] == min_id + other[0] and edge['to_node_id'] == min_id + other[1]) for other in EDGES_TO_CREATE])


def test_add_node():
	response = client.post('/nodes', json={})
	assert response.status_code == 201
	json_data = response.json()

	assert len(json_data) == 1
	node = json_data[0]

	assert node in get_graph_nodes()


def test_delete_node():
	max_id = get_max_id()

	response = client.request('DELETE', '/nodes', json={'node_id': max_id})
	assert response.status_code == 204

	assert {'node_id': max_id} not in get_graph_nodes()


def test_node_connected():
	seed_graph()

	first_node = get_min_id()

	response = client.get(f'/nodes/{first_node}/connected')
	assert response.status_code == 200
	json_data = response.json()
	assert list(map(lambda node: node['id'], json_data)) == list(map(lambda node: node['id'] + first_node - 1,
																	 [{'id':1},
																	  {'id':2},
																	  {'id':3},
																	  {'id':5},
																	  {'id':6},
																	  {'id':4},
																	  {'id':7},
																	  {'id':8},
																	  {'id':9},
																	  {'id':13},
																	  {'id':11},
																	  {'id':14},
																	  {'id':15},
																	  {'id':16},
																	  {'id':10},
																	  {'id':12}]))
