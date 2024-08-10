from pydantic import BaseModel
from fastapi import Query


class Pagination(BaseModel):
    skip: int = Query(0, ge=0)
    limit: int = Query(10, ge=0)


class PaginationResponse(Pagination):
    total: int
