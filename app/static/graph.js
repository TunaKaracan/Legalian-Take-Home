let selectedNode = null;
let lastTapTime = 0;

const cy = cytoscape({
	container: document.getElementById('cy'),
	elements: [],
	style: [
		{
		selector: 'node',
		style: {
			'label': 'data(id)',
			'text-valign': 'center',
			'text-halign': 'center',
			'color': '#fff',
			'text-outline-width': 1,
			'text-outline-color': '#111',
			'background-color': '#0074D9'
		}
		},
		{
		selector: 'edge',
		style: {
			'width': 2,
			'line-color': '#aaa',
			'target-arrow-shape': 'triangle',
			'curve-style': 'bezier'
		}
		},
		{
		selector: ':selected',
		style: {
			'background-color': 'red'
		}
		},
		{
		selector: '.connected',
		style: {
			'background-color': 'orange'
		}
		}
	],
	layout: {name:'cose'}
});

function getGraph() {
	fetch("/graph").then((resp) => {
		resp.json().then((r) => {
			for(let i = 0; i < r["nodes"].length; i++){
				let node = r["nodes"][i]
				addNode(node["id"])
			}
			for(let i = 0; i < r["edges"].length; i++){
				let edge = r["edges"][i]
				addEdge(edge["id"], edge["from_node_id"], edge["to_node_id"])
			}
			let layout = cy.layout({ name: "cose-bilkent",
				animate: true,
				animationEasing: 'ease-out',
				animationDuration: 1000,
				
				nodeRepulsion: 1000,
				edgeElasticity: 0.45,
				gravity: 0.25});
			layout.run()
		})
	});
}

function seedGraph(url) {
	fetch(url, {
		method: 'POST',
		headers: {'content-type': 'application/json'}
	}).then(() => {
		cy.elements().remove();
		getGraph();
		selectedNode = null;
	});
}

function addNode(id, position){
	cy.add({
		group: "nodes",
		data: {id: `${id}`},
		position: position
	});
}

function addEdge(id, source, target){
	cy.add({
		data: {
			id: `e${id}`,
			source: `${source}`,
			target: `${target}`
		}
	})
}

function resetConnected(){
	cy.nodes().removeClass('connected');
}

function resetNodeStates(){
	resetConnected();
	if(selectedNode){
		selectedNode.selectify().unselect().unselectify();
		selectedNode = null;
	}
}

// Click node -> select / create edge
cy.on('tap', 'node', evt => {
	const node = evt.target;

	if (!selectedNode) {
		node.selectify().select().unselectify();
		selectedNode = node;

		fetch(`/nodes/${node.id()}/connected`, {
			method: 'GET',
			headers: {'content-type': 'application/json'}
		}).then((resp) => {
			resp.json().then((r) => {
				for(let i = 0; i < r.length; i++){
					let id = r[i]['id']
					let c_node = cy.nodes(`#${id}`);
					if (id != node.id())
						c_node.addClass('connected');
				}
			})
		});
	} else {
		fetch('/edges', {
			method: 'POST',
			body: JSON.stringify({
						from_node_id: selectedNode.id(),
						to_node_id: node.id()
					}),
			headers: {'content-type': 'application/json'}
		}).then((resp) => {
			resp.json().then((r) => {
				cy.add({
					group: 'edges',
					data: {
						id: `e${r[0]["id"]}`,
						source: selectedNode.id(),
						target: node.id()
					}
				});
				cy.elements().selectify().unselect().unselectify();
				resetNodeStates();
			})
		});
	}
});

// Double-click on background -> create node
cy.on('tap', evt => {
	const now = Date.now();
	const isDoubleClick = (now - lastTapTime) < 200;
	lastTapTime = now;


	if (evt.target === cy && isDoubleClick) {
		fetch('/nodes', {
				method: 'POST',
				body: '{}',
				headers: {'content-type': 'application/json'}
		}).then((resp) => {
			resp.json().then((r) => {
				let id = r[0]['id']
				addNode(id, evt.position);
			})
		});
	}
});

// Click background -> clear selection
cy.on('tap', evt => {
	if (evt.target === cy)
		resetNodeStates();
});

// Right click -> delete node
cy.on('cxttap', 'node', evt => {
	resetNodeStates();

	const node = evt.target;

	fetch('/nodes', {
		method: 'DELETE',
		body: JSON.stringify({
			node_id: node.id()
		}),
		headers: {'content-type': 'application/json'}
	}).then(() => {
		evt.target.remove();
	});
});

// Left click -> swap edge direction
cy.on('tap', 'edge', evt => {
	resetNodeStates();

	let edge = evt.target;

	fetch('/edges', {
		method: 'PUT',
		body: JSON.stringify({
			edge_id: edge.id().slice(1)
		}),
		headers: {'content-type': 'application/json'}
	}).then(() => {
		edge.move({
			source: edge.target().id(),
			target: edge.source().id()
		});
	});

	edge.unselectify();
});

// Right click -> delete edge
cy.on('cxttap', 'edge', evt => {
	resetNodeStates();

	const edge = evt.target;

	fetch('/edges', {
		method: 'DELETE',
		body: JSON.stringify({
			edge_id: edge.id().slice(1)
		}),
		headers: {'content-type': 'application/json'}
	}).then(() => {
		evt.target.remove();
	});
});

document.getElementById('btnClear').addEventListener('click', () => {
	fetch('/graph/clear', {
		method: 'DELETE',
		headers: {'content-type': 'application/json'}
	}).then(() => {
		cy.elements().remove();
		selectedNode = null;
	});
});

document.getElementById('btnSeedD').addEventListener('click', () => {
	seedGraph('/graph/seed')
});

document.getElementById('btnSeedR').addEventListener('click', () => {
	seedGraph('/graph/seed_random')
});

getGraph();
