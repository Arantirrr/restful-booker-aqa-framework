from pydantic import BaseModel


class ValidationErrorResponse(BaseModel):
    errors: list[str]

class ConflictErrorResponse(BaseModel):
    error: str