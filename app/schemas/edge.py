from pydantic import BaseModel, PositiveInt

class EdgeBase(BaseModel):
	from_node_id: PositiveInt
	to_node_id: PositiveInt

class EdgeCreate(EdgeBase):
	pass

class EdgeResponse(EdgeBase):
	id: PositiveInt

class EdgeDeleteRequest(BaseModel):
	edge_id: PositiveInt

class EdgeSwapRequest(BaseModel):
	edge_id: PositiveInt