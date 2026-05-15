"""
Comprehensive Analysis Endpoints
Endpoints for complete FIR analysis
"""

from fastapi import APIRouter, status
import time
from app.models.schemas import FIRAnalysisRequest, FIRAnalysisResponse
from app.services.preprocessing import preprocessing_service
from app.services.ner import ner_service
from app.services.ppc_mapper import ppc_mapping_service
from app.services.timeline import timeline_service

router = APIRouter()


@router.post(
    "/analyze-fir",
    response_model=FIRAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Complete FIR Analysis",
    description="Perform comprehensive analysis of Urdu FIR text"
)
async def analyze_fir(request: FIRAnalysisRequest) -> FIRAnalysisResponse:
    """
    Perform comprehensive FIR analysis
    
    Combines preprocessing, entity extraction, PPC mapping, and timeline generation
    
    Args:
        request: FIRAnalysisRequest with analysis options
        
    Returns:
        FIRAnalysisResponse with complete analysis results
    """
    start_time = time.time()
    
    preprocessing_result = None
    entities_result = None
    ppc_result = None
    timeline_result = None
    
    try:
        # Step 1: Preprocessing
        if request.include_preprocessing:
            preprocessing_result = preprocessing_service.preprocess(
                text=request.fir_text,
                fir_id=request.fir_id
            )
        
        # Step 2: Entity Extraction
        if request.include_entities:
            entities_result = ner_service.extract_entities(
                text=request.fir_text,
                fir_id=request.fir_id
            )
        
        # Step 3: PPC Mapping
        if request.include_ppc:
            ppc_result = ppc_mapping_service.map_ppc_sections(
                text=request.fir_text,
                entities=entities_result.entities if entities_result else None,
                fir_id=request.fir_id
            )
        
        # Step 4: Timeline Generation
        if request.include_timeline:
            timeline_result = timeline_service.generate_timeline(
                text=request.fir_text,
                entities=entities_result.entities if entities_result else None,
                fir_id=request.fir_id
            )
        
        # Calculate overall confidence
        confidences = []
        if preprocessing_result:
            confidences.append(0.8)  # Preprocessing confidence
        if entities_result:
            confidences.append(entities_result.extraction_confidence)
        if ppc_result:
            confidences.append(ppc_result.analysis_confidence)
        if timeline_result:
            confidences.append(timeline_result.reconstruction_confidence)
        
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        return FIRAnalysisResponse(
            fir_id=request.fir_id,
            preprocessing=preprocessing_result,
            entities=entities_result,
            ppc_mapping=ppc_result,
            timeline=timeline_result,
            overall_confidence=overall_confidence,
            total_processing_time_ms=processing_time_ms
        )
        
    except Exception as e:
        processing_time_ms = (time.time() - start_time) * 1000
        raise
