"""
FIR Processing Endpoints
Endpoints for processing Urdu FIR text
"""

from fastapi import APIRouter, status, HTTPException
from app.models.schemas import (
    FIRPreprocessRequest, FIRPreprocessResponse,
    FIREntityExtractionResponse,
    PPCMappingRequest, PPCMappingResponse,
    TimelineGenerationRequest, TimelineGenerationResponse
)
from app.services.preprocessing import preprocessing_service
from app.services.ner import ner_service
from app.services.ppc_mapper import ppc_mapping_service
from app.services.timeline import timeline_service

router = APIRouter()


@router.post(
    "/preprocess",
    response_model=FIRPreprocessResponse,
    status_code=status.HTTP_200_OK,
    summary="Preprocess FIR Text",
    description="Clean, normalize, and tokenize Urdu FIR text"
)
async def preprocess_fir(request: FIRPreprocessRequest) -> FIRPreprocessResponse:
    """
    Preprocess Urdu FIR text
    
    Issue #2: Urdu text preprocessing
    
    Args:
        request: FIRPreprocessRequest with FIR text
        
    Returns:
        FIRPreprocessResponse with preprocessed text and metadata
    """
    return preprocessing_service.preprocess(
        text=request.fir_text,
        fir_id=request.fir_id
    )


@router.post(
    "/extract-entities",
    response_model=FIREntityExtractionResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract Entities",
    description="Extract named entities (persons, locations, crimes) from FIR text"
)
async def extract_entities(request: FIRPreprocessRequest) -> FIREntityExtractionResponse:
    """
    Extract named entities from FIR text
    
    Issue #3: Entity extraction module
    
    Args:
        request: FIRPreprocessRequest with FIR text
        
    Returns:
        FIREntityExtractionResponse with extracted entities
    """
    return ner_service.extract_entities(
        text=request.fir_text,
        fir_id=request.fir_id
    )


@router.post(
    "/map-ppc",
    response_model=PPCMappingResponse,
    status_code=status.HTTP_200_OK,
    summary="Map to PPC Sections",
    description="Map FIR to applicable Penal Code (PPC) sections"
)
async def map_ppc(request: PPCMappingRequest) -> PPCMappingResponse:
    """
    Map FIR to PPC sections
    
    Issue #4: PPC mapping basic
    
    Args:
        request: PPCMappingRequest with FIR text and optional entities
        
    Returns:
        PPCMappingResponse with suggested PPC sections
    """
    return ppc_mapping_service.map_ppc_sections(
        text=request.fir_text,
        entities=request.entities,
        fir_id=request.fir_id
    )


@router.post(
    "/generate-timeline",
    response_model=TimelineGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Timeline",
    description="Generate event timeline from FIR text"
)
async def generate_timeline(request: TimelineGenerationRequest) -> TimelineGenerationResponse:
    """
    Generate event timeline from FIR
    
    Issue #5: Timeline generation
    
    Args:
        request: TimelineGenerationRequest with FIR text and optional entities
        
    Returns:
        TimelineGenerationResponse with reconstructed timeline
    """
    return timeline_service.generate_timeline(
        text=request.fir_text,
        entities=request.entities,
        fir_id=request.fir_id
    )
