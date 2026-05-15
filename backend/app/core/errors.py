"""
Custom Exceptions and Error Handling
Defines application-specific exceptions
"""

from typing import Optional, Dict, Any


class LegalReconException(Exception):
    """
    Base exception for Legal Recon application
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "GENERAL_ERROR",
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize exception
        
        Args:
            message: Error message
            error_code: Machine-readable error code
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class PreprocessingError(LegalReconException):
    """
    Raised when text preprocessing fails
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="PREPROCESSING_ERROR",
            status_code=400,
            details=details
        )


class EntityExtractionError(LegalReconException):
    """
    Raised when entity extraction fails
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="ENTITY_EXTRACTION_ERROR",
            status_code=400,
            details=details
        )


class PPCMappingError(LegalReconException):
    """
    Raised when PPC mapping fails
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="PPC_MAPPING_ERROR",
            status_code=400,
            details=details
        )


class TimelineGenerationError(LegalReconException):
    """
    Raised when timeline generation fails
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="TIMELINE_GENERATION_ERROR",
            status_code=400,
            details=details
        )


class ValidationError(LegalReconException):
    """
    Raised when validation fails
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class ModelNotFoundError(LegalReconException):
    """
    Raised when NLP model is not found
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="MODEL_NOT_FOUND",
            status_code=500,
            details=details
        )
