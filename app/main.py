from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.handlers import node_not_found_handler, edge_not_found_handler
from app.core import exceptions
from app.api.router import api_router
from app.core.config import settings

docs_url = '/docs' if settings.debug_mode else None
redoc_url = '/redoc' if settings.debug_mode else None
server = FastAPI(title=settings.name,
				 debug=settings.debug_mode,
				 docs_url=docs_url,
				 redoc_url=redoc_url)

server.add_exception_handler(exceptions.NodeNotFoundError, node_not_found_handler)
server.add_exception_handler(exceptions.EdgeNotFoundError, edge_not_found_handler)

server.include_router(api_router)

server.mount('/', StaticFiles(directory='app/static', html=True), name='static')
