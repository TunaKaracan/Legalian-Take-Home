from fastapi import APIRouter
from app.api.routers import graph, node, edge

api_router = APIRouter()

api_router.include_router(graph.router, prefix='/graph', tags=['Graph'])
api_router.include_router(node.router, prefix='/nodes', tags=['Nodes'])
api_router.include_router(edge.router, prefix='/edges', tags=['Edges'])
