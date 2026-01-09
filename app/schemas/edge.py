from typing_extensions import Annotated
from pydantic import BaseModel, PositiveInt, Field

class EdgeBase(BaseModel):
	from_node_id: int
	to_node_id: int

class EdgeCreate(EdgeBase):
	pass

class EdgeResponse(EdgeBase):
	id: int

class EdgeDeleteRequest(BaseModel):
	edge_ids: Annotated[list[PositiveInt], Field(min_length=1)]

class EdgeSwapRequest(BaseModel):
	edge_id: int