from typing_extensions import Annotated
from pydantic import BaseModel, PositiveInt, Field

class NodeCreate(BaseModel):
    pass

class NodeResponse(BaseModel):
    id: int

class NodeDeleteRequest(BaseModel):
    node_ids: Annotated[list[PositiveInt], Field(min_length=1)]
