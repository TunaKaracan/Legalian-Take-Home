# Legalian - Take Home - Graph API

A simple Graph API built with **FastAPI** that allows you to create nodes and edges to explore
relationships between nodes in a graph. The service runs via **Docker Compose** and uses
**MySQL** for persistence.

---

### Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Design Decisions & Trade-offs](#design-decisions--trade-offs)
4. [Running the Project](#running-the-project)
5. [Testing](#testing)
6. [Connectivity & Graph Operations](#connectivity--graph-operations)
7. [Interactive Frontend](#interactive-frontend)

## Overview
This project implements a minimal but well-structured graph service intended for an MVP-sized
system. The focus is on:
- Clear separation of concerns
- Deterministic and atomic graph operations
- Efficient graph traversal at the database level
- An interactive graph UI

## Architecture

This service is implemented as a layered **FastAPI** application, designed to clearly separate
**HTTP concerns, business logic, and persistence**. The architecture prioritizes readability,
testability, and maintainability while remaining intentionally simple for an MVP-sized system.

The codebase is organized into the following layers:

- **API layer** (`api/`): Defines HTTP routes and contains no business logic and delegates all work to the service layer.
- **Service layer** (`services/`): Encapsulates application and domain logic, including validation and orchestration.
- **Repository layer** (`repositories/`): Responsible for all database interactions and persistence logic.
- **Models** (`models/`): SQLAlchemy ORM models representing database tables.
- **Schemas** (`schemas/`): Pydantic models used for request validation and response serialization.
- **Core** (`core/`): Application configuration, database setup and exception definitions.

#### Graph Traversal
Graph traversal is implemented using a recursive Common Table Expression (CTE) in MySQL,
enabling deep connectivity queries to be executed in a single database query.

---

#### Error Handling
Validation errors are handled through Pydantic schemas, domain-specific exceptions are raised in the
service layer and translated into appropriate HTTP responses using FastAPI exception handlers.

## Design Decisions & Trade-offs

#### Clear Layered Architecture
A clear API-service-repository separation was preferred since it improves testability, readability,
and scalability for larger codebases, even though it introduces additional boilerplate.

---

#### Explicit Error Handling
Resource existence is explicitly validated in the service layer instead of relying on database
constraint errors. This improves error clarity and API behavior at the cost of additional queries.

---

#### Bulk Operations
Bulk operations were preferred over single-resource endpoints to keep the API surface
minimal and support more efficient graph updates with singular queries.

---

#### Atomic Operations
Atomic graph operations were preferred since graph consistency was prioritized over partial
success, ensuring the system is never left in an intermediate or invalid state. The tradeoff
is reduced flexibility, as all errors must be resolved before requests.

---

#### No Asyncio
The API uses synchronous SQLAlchemy sessions instead of async sessions. This simplifies
transaction handling for a take-home project, at the cost of reduced concurrency under load.

## Running the Project

#### Requirements

* Docker
* Docker Compose plugin

#### Start the Services

The example Docker Compose file can be found at `docker-compose.example.yml`.
Run the following command from the project root:

```shell
docker compose -f docker-compose.example.yml up -d
```

This will start:

* A MySQL database instance
* The FastAPI application

---

#### Configuration

The application can be configured using the following environment variables:

| Variable          | Description                    | Default     |
|-------------------|--------------------------------|-------------|
| `PORT`            | FastAPI server port            | 8000        |
| `APP_NAME`        | FastAPI application title      | Legalian... |
| `APP_DEBUG_MODE`  | Enable/disable Swagger & Redoc | True        |
| `APP_DB_HOST`     | Database host                  | localhost   |
| `APP_DB_PORT`     | Database port                  | 3306        |
| `APP_DB_USER`     | Database user                  | root        |
| `APP_DB_PASSWORD` | Database password              | 1234        |
| `APP_DB_NAME`     | Database name                  | graph_db    |

#### API Documentation

Once running, if `APP_DEBUG_MODE` is not `False`, you can access the interactive API
documentation at:

- `http://localhost:<PORT>/docs` or
- `http://localhost:<PORT>/redoc`

## Testing
To verify the API is functioning correctly, run the test suite from the project root:
```shell
pytest -v
```

Expected output:
```shell
app/tests/test_graph.py::test_clear_graph PASSED      [ 20%]
app/tests/test_graph.py::test_seed_graph PASSED       [ 40%]
app/tests/test_graph.py::test_add_node PASSED         [ 60%]
app/tests/test_graph.py::test_delete_node PASSED      [ 80%]
app/tests/test_graph.py::test_node_connected PASSED   [100%]
```

## Connectivity & Graph Operations

#### 1. Verify the Database & API Are Running

To confirm the database and API are running, execute the following `cURL` command:
```shell
curl -X 'GET' 'http://127.0.0.1:<PORT>/graph' -H 'accept: application/json'
```

Expected response for an empty graph:
```json
{
  "nodes":[],
  "edges":[]
}
```

---

#### 2. Seed the Graph

Next, initialize the graph with a predefined state:

```shell
curl -X 'POST' 'http://127.0.0.1:<PORT>/graph/seed' -H 'accept: application/json'
```
This will populate the graph with a known set of nodes and edges for testing and development.

---

#### 3. Get Connected Nodes

Retrieve all nodes reachable from a given node (including itself):
```http
GET /nodes/{node_id}/connected
```

Example for node with `id = 1`:
```shell
curl -X 'GET' 'http://127.0.0.1:<PORT>/nodes/1/connected' -H 'accept: application/json'
```

Response:
```json
[
  {"id":1},
  {"id":2},
  {"id":3},
  {"id":5},
  {"id":6},
  {"id":4},
  {"id":7},
  {"id":8},
  {"id":9},
  {"id":13},
  {"id":11},
  {"id":14},
  {"id":15},
  {"id":16},
  {"id":10},
  {"id":12}
]
```

## Interactive Frontend

An interactive graph UI is available at:
- `http://localhost:<PORT>`

![frontend](https://chibi.kutuptilkisi.dev/su3IoJqUKO7B.png)

Features:
- **Add nodes:** Double-click anywhere on the canvas to insert a new node into the graph.
- **Explore reachability:** Click on a node to highlight all nodes reachable from it with orange.
- **Create edges:** While a node is selected, click on another node to create a directed connection between them.
- **Remove elements:** Right-click on a node or an edge to remove it.
- **Reverse edges:** Click on an edge to swap its direction.
- **Clear graph:** Use the Clear Graph button to remove all nodes and edges.
- **Seed graph:** Use the Seed Graph button to initialize the graph with a predefined state.
- **Generate random graph:** Use the Seed Random Graph button to create a graph with a randomly generated state.
