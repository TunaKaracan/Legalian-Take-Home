from pydantic import BaseModel, PositiveInt

class EdgeBase(BaseModel):
	from_node_id: int
	to_node_id: int

class EdgeCreate(EdgeBase):
	pass

class EdgeResponse(EdgeBase):
	id: int

class EdgeDeleteRequest(BaseModel):
	edge_id: PositiveInt

class EdgeSwapRequest(BaseModel):
	edge_id: int