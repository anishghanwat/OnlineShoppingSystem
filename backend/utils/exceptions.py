"""Custom exception classes for the application."""


class AppException(Exception):
    """Base exception class for application errors."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class BadRequestException(AppException):
    """Exception raised for bad requests."""
    
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=400)


class UnauthorizedException(AppException):
    """Exception raised for unauthorized access."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    """Exception raised for forbidden access."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class InsufficientStockException(AppException):
    """Exception raised when product stock is insufficient."""
    
    def __init__(self, message: str = "Insufficient stock"):
        super().__init__(message, status_code=400)


class ValidationException(AppException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)
