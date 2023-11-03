from typing import (
    Generic, 
    TypeVar, 
    Optional, 
    List
)

from pydantic import BaseModel



T = TypeVar("T")
class ResponseSchema(BaseModel):
    status: Optional[int]
    detail: Optional[str]
    result: Optional[T] = None



class PaginationSchema(BaseModel, Generic[T]):
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]