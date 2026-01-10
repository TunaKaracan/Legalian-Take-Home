from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core import exceptions


async def node_not_found_handler(request: Request,
								 exc: exceptions.NodeNotFoundError) -> JSONResponse:
	return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
						content={'detail': str(exc)})


async def edge_not_found_handler(request: Request,
								 exc: exceptions.EdgeNotFoundError) -> JSONResponse:
	return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
						content={'detail': str(exc)})
