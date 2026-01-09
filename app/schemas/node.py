from pydantic import BaseModel, PositiveInt

class NodeCreate(BaseModel):
    pass

class NodeResponse(BaseModel):
    id: PositiveInt

class NodeDeleteRequest(BaseModel):
    node_id: PositiveInt
