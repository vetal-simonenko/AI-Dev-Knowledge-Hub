from fastapi import APIRouter

from app.schemas.tools import AddNumbersRequest, AddNumbersResponse
from app.tools.calculator import add_numbers

router = APIRouter(
    prefix="/tools",
    tags=["Tools"],
)


@router.post("/add", response_model=AddNumbersResponse)
def add(request: AddNumbersRequest) -> AddNumbersResponse:
    result = add_numbers(
        a=request.a,
        b=request.b,
    )

    return AddNumbersResponse(result=result)
