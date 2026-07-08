from pydantic import BaseModel


class AddNumbersRequest(BaseModel):
    a: float
    b: float


class AddNumbersResponse(BaseModel):
    result: float
