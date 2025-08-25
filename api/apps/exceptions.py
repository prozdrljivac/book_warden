from fastapi import HTTPException


class HTTP404Exception(HTTPException):
    """Raised when route cannot be found"""
    def __init__(self, detail) -> None:
        super().__init__(status_code=404, detail=detail)

class BusinessRuleException(ValueError):
    """Raised when a Business Rule is not meet"""
