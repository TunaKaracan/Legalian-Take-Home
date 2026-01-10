from fastapi import FastAPI

from app.api.handlers import node_not_found_handler, edge_not_found_handler
from app.core import exceptions
from app.api.graph import router as nodes_router
from app.core.config import settings


server = FastAPI(title=settings.name, debug=settings.debug_mode)

server.add_exception_handler(exceptions.NodeNotFoundError, node_not_found_handler)
server.add_exception_handler(exceptions.EdgeNotFoundError, edge_not_found_handler)

server.include_router(nodes_router)
