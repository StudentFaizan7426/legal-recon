"""
PPC (Penal Code) Mapping Service
Maps extracted entities and crime descriptions to relevant legal sections

Issue #4: PPC mapping basic
"""

import logging
from typing import List, Dict
from app.models.schemas import PPCSection, PPCMappingResponse, Entity
from app.core.errors import PPCMappingError

logger = logging.getLogger(__name__)


class PPCMappingService:
    """
    Service for mapping crimes to Penal Code sections
    """
    
    # Basic PPC sections database
    # TODO: Expand with comprehensive PPC sections
    PPC_DATABASE = {
        "302": {
            "title": "Murder",
            "punishment": "Death or life imprisonment",
            "keywords": ["قتل", "murder", "death"]
        },
        "304": {
            "title": "Death by negligence",
            "punishment": "Imprisonment up to 2 years",
            "keywords": ["احتیاط کی کمی", "negligence"]
        },
        "380": {
            "title": "Theft",
            "punishment": "Imprisonment up to 7 years",
            "keywords": ["چوری", "theft", "stealing"]
        },
        "379": {
            "title": "Punishment for theft",
            "punishment": "Imprisonment up to 3 years",
            "keywords": ["چوری کی سزا", "theft punishment"]
        },
        "397": {
            "title": "Punishment for dacoity",
            "punishment": "Life or 14 years imprisonment",
            "keywords": ["ڈکیتی", "dacoity", "robbery"]
        },
        "506": {
            "title": "Criminal intimidation",
            "punishment": "Imprisonment up to 2 years",
            "keywords": ["دھمکی", "intimidation", "threat"]
        }
    }
    
    def __init__(self):
        """Initialize PPC mapping service"""
        logger.info("Initializing PPCMappingService")
        # TODO: Load comprehensive PPC database
        # self.ppc_db = self._load_ppc_database()
    
    def map_ppc_sections(self, text: str, entities: List[Entity] = None, fir_id: str = None) -> PPCMappingResponse:
        """
        Map FIR to applicable PPC sections
        
        Args:
            text: FIR text
            entities: Extracted entities (optional)
            fir_id: FIR identifier
            
        Returns:
            PPCMappingResponse with suggested sections
            
        Raises:
            PPCMappingError: If mapping fails
        """
        try:
            if not text or len(text.strip()) == 0:
                raise PPCMappingError("FIR text cannot be empty")
            
            # Find matching PPC sections
            matched_sections = self._match_sections(text, entities)
            
            # Sort by relevance
            matched_sections.sort(key=lambda x: x.relevance_score, reverse=True)
            
            primary = matched_sections[0] if matched_sections else None
            secondary = matched_sections[1:] if len(matched_sections) > 1 else []
            
            # Calculate overall confidence
            confidences = [s.relevance_score for s in matched_sections] if matched_sections else [0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            logger.info(f"Mapped {len(matched_sections)} PPC sections")
            
            return PPCMappingResponse(
                fir_id=fir_id,
                suggested_sections=matched_sections,
                primary_section=primary,
                secondary_sections=secondary,
                total_matching_sections=len(matched_sections),
                analysis_confidence=avg_confidence
            )
            
        except PPCMappingError:
            raise
        except Exception as e:
            logger.error(f"PPC mapping error: {str(e)}")
            raise PPCMappingError(
                message=f"Failed to map PPC sections: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _match_sections(self, text: str, entities: List[Entity] = None) -> List[PPCSection]:
        """
        Match text against PPC sections
        
        TODO: Implement intelligent matching
        - Keyword-based matching
        - ML-based relevance scoring
        - Entity-based section matching
        """
        matched = []
        text_lower = text.lower()
        
        for section_num, section_data in self.PPC_DATABASE.items():
            # Simple keyword matching (placeholder)
            match_score = 0
            for keyword in section_data["keywords"]:
                if keyword.lower() in text_lower:
                    match_score += 0.5
            
            if match_score > 0:
                matched.append(PPCSection(
                    section_number=section_num,
                    section_title=section_data["title"],
                    punishment=section_data["punishment"],
                    relevance_score=min(match_score, 1.0),
                    description=section_data["title"]
                ))
        
        return matched


# Global PPC mapping service instance
ppc_mapping_service = PPCMappingService()
