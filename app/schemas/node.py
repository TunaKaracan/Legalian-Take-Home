from pydantic import BaseModel, PositiveInt

class NodeCreate(BaseModel):
    pass

class NodeResponse(BaseModel):
    id: int

class NodeDeleteRequest(BaseModel):
    node_id: PositiveInt
