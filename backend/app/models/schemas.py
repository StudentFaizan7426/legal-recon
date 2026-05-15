"""
Pydantic Schemas for Request/Response Validation
Ensures type safety and automatic validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============ Base Models ============

class ResponseModel(BaseModel):
    """Base response model"""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    message: str
    error_code: str
    details: Optional[Dict[str, Any]] = None


# ============ FIR Related Models ============

class FIRPreprocessRequest(BaseModel):
    """Request model for FIR text preprocessing"""
    fir_text: str = Field(..., min_length=1, description="Raw Urdu FIR text")
    fir_id: Optional[str] = Field(None, description="FIR identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "fir_text": "یہ ایک نمونہ اردو متن ہے",
                "fir_id": "FIR-2024-001"
            }
        }


class FIRPreprocessResponse(BaseModel):
    """Response model for FIR preprocessing"""
    original_text: str
    preprocessed_text: str
    text_length: int
    token_count: int
    language_detected: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Entity(BaseModel):
    """Individual entity extracted from text"""
    text: str = Field(..., description="Entity text")
    entity_type: str = Field(..., description="Type of entity (PERSON, LOCATION, CRIME, etc.)")
    confidence: float = Field(default=0.0, ge=0, le=1, description="Confidence score")
    start_pos: int = Field(..., description="Start position in text")
    end_pos: int = Field(..., description="End position in text")


class FIREntityExtractionResponse(BaseModel):
    """Response model for entity extraction"""
    fir_id: Optional[str]
    entities: List[Entity]
    entity_count: int
    extraction_confidence: float = Field(default=0.0, ge=0, le=1)
    processing_time_ms: float


class RelationshipType(str, Enum):
    """Types of relationships between entities"""
    ACCUSED_OF = "accused_of"
    VICTIM_OF = "victim_of"
    WITNESS_TO = "witness_to"
    LOCATION_OF = "location_of"
    INVOLVED_IN = "involved_in"


class EntityRelationship(BaseModel):
    """Relationship between two entities"""
    source_entity: str
    target_entity: str
    relationship_type: RelationshipType
    confidence: float = Field(default=0.0, ge=0, le=1)


# ============ PPC Mapping Models ============

class PPCSection(BaseModel):
    """PPC (Penal Code) section suggestion"""
    section_number: str = Field(..., description="PPC section number (e.g., '302')")
    section_title: str = Field(..., description="Title of the section")
    punishment: str = Field(..., description="Punishment details")
    relevance_score: float = Field(default=0.0, ge=0, le=1, description="Relevance to FIR")
    description: str = Field(..., description="Section description")


class PPCMappingRequest(BaseModel):
    """Request model for PPC mapping"""
    fir_text: str = Field(..., min_length=1, description="FIR text for analysis")
    entities: Optional[List[Entity]] = Field(None, description="Pre-extracted entities")
    fir_id: Optional[str] = None


class PPCMappingResponse(BaseModel):
    """Response model for PPC mapping"""
    fir_id: Optional[str]
    suggested_sections: List[PPCSection]
    primary_section: Optional[PPCSection]
    secondary_sections: List[PPCSection]
    total_matching_sections: int
    analysis_confidence: float = Field(default=0.0, ge=0, le=1)


# ============ Timeline Models ============

class TimelineEvent(BaseModel):
    """Individual event in a timeline"""
    event_id: str = Field(..., description="Unique event identifier")
    event_description: str = Field(..., description="Description of the event")
    timestamp: Optional[datetime] = Field(None, description="When the event occurred")
    location: Optional[str] = Field(None, description="Where the event occurred")
    entities_involved: List[str] = Field(default_factory=list, description="Entities involved")
    confidence: float = Field(default=0.0, ge=0, le=1, description="Confidence in event extraction")
    source_text_span: Optional[str] = Field(None, description="Original text excerpt")


class TimelineGenerationRequest(BaseModel):
    """Request model for timeline generation"""
    fir_text: str = Field(..., min_length=1, description="FIR text")
    entities: Optional[List[Entity]] = Field(None, description="Pre-extracted entities")
    fir_id: Optional[str] = None


class TimelineGenerationResponse(BaseModel):
    """Response model for timeline generation"""
    fir_id: Optional[str]
    timeline_events: List[TimelineEvent]
    event_sequence: List[str] = Field(description="Chronological event IDs")
    start_event: Optional[str]
    end_event: Optional[str]
    temporal_coverage_days: Optional[int]
    reconstruction_confidence: float = Field(default=0.0, ge=0, le=1)


# ============ Comprehensive Analysis Models ============

class FIRAnalysisRequest(BaseModel):
    """Request model for complete FIR analysis"""
    fir_text: str = Field(..., min_length=1, description="Raw Urdu FIR text")
    fir_id: Optional[str] = Field(None, description="FIR identifier")
    include_preprocessing: bool = Field(default=True, description="Include text preprocessing")
    include_entities: bool = Field(default=True, description="Include entity extraction")
    include_ppc: bool = Field(default=True, description="Include PPC mapping")
    include_timeline: bool = Field(default=True, description="Include timeline generation")


class FIRAnalysisResponse(BaseModel):
    """Complete FIR analysis response"""
    fir_id: Optional[str]
    preprocessing: Optional[FIRPreprocessResponse] = None
    entities: Optional[FIREntityExtractionResponse] = None
    ppc_mapping: Optional[PPCMappingResponse] = None
    timeline: Optional[TimelineGenerationResponse] = None
    overall_confidence: float = Field(default=0.0, ge=0, le=1)
    total_processing_time_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============ Health Check Models ============

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy")
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
