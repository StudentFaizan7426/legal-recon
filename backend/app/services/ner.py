"""
Named Entity Recognition (NER) Service
Extracts entities like persons, locations, organizations, crimes from Urdu text

Issue #3: Entity extraction module
"""

import logging
import re
from typing import List, Dict
from app.models.schemas import Entity, FIREntityExtractionResponse
from app.core.errors import EntityExtractionError
import time

logger = logging.getLogger(__name__)


class NERService:
    """
    Named Entity Recognition service for Urdu text
    Extracts legal entities relevant to FIRs
    """
    
    # Entity types relevant to legal FIRs
    ENTITY_TYPES = [
        "PERSON",      # Names of people (complainant, accused, witness, victim)
        "LOCATION",    # Geographic locations (addresses, police stations)
        "CRIME",       # Type of crime
        "ORGANIZATION", # Police stations, courts, government offices
        "TIME",        # Dates and times of incident
        "WEAPON",      # Weapons or tools used
        "EVIDENCE",    # Evidence mentioned
        "VEHICLE",     # Vehicles involved
    ]
    
    # Urdu keywords for entity detection
    URDU_KEYWORDS = {
        "CRIME": {
            'کلیدی الفاظ': [
                'قتل', 'چوری', 'لوٹ', 'ڈاکیتی', 'زیادتی', 'دھمکی', 'فریب',
                'جعل', 'مار', 'پیٹ', 'ہتھیار', 'چاقو', 'بندوق'
            ],
            'انگریزی الفاظ': [
                'murder', 'theft', 'robbery', 'rape', 'assault', 'fraud',
                'forgery', 'blackmail', 'weapon', 'shooting'
            ]
        },
        "LOCATION": {
            'کلیدی الفاظ': [
                'تھانہ', 'شہر', 'گاؤں', 'سڑک', 'گھر', 'دفتر', 'بازار',
                'پاکستان', 'کراچی', 'لاہور', 'اسلام آباد'
            ],
            'انگریزی الفاظ': [
                'police station', 'city', 'village', 'road', 'house', 'office',
                'market', 'pakistan', 'karachi', 'lahore', 'islamabad'
            ]
        },
        "PERSON": {
            'کلیدی الفاظ': [
                'مجرم', 'ملزم', 'شکایت کنندہ', 'گواہ', 'متاثر',
                'پولیس', 'کانسٹیبل'
            ],
            'انگریزی الفاظ': [
                'accused', 'complainant', 'witness', 'victim', 'police', 'constable'
            ]
        },
        "ORGANIZATION": {
            'کلیدی الفاظ': [
                'پولیس', 'عدالت', 'تھانہ', 'وکیل', 'جج'
            ],
            'انگریزی الفاظ': [
                'police', 'court', 'station', 'lawyer', 'judge'
            ]
        },
        "TIME": {
            'کلیدی الفاظ': [
                'رات', 'دن', 'صبح', 'شام', 'جنوری', 'فروری',
                'آج', 'کل', 'پچھلے'
            ],
            'انگریزی الفاظ': [
                'night', 'day', 'morning', 'evening', 'january', 'february',
                'today', 'yesterday', 'last', 'time', 'date'
            ]
        }
    }
    
    def __init__(self):
        """Initialize NER service"""
        logger.info("✓ Initializing NERService")
    
    def extract_entities(self, text: str, fir_id: str = None) -> FIREntityExtractionResponse:
        """
        Extract named entities from Urdu FIR text
        
        Uses keyword-based and pattern-based extraction with rule-based confidence scoring
        
        Args:
            text: Preprocessed Urdu text
            fir_id: Optional FIR identifier
            
        Returns:
            FIREntityExtractionResponse with extracted entities
            
        Raises:
            EntityExtractionError: If extraction fails
        """
        start_time = time.time()
        
        try:
            if not text or len(text.strip()) == 0:
                raise EntityExtractionError("Text cannot be empty")
            
            logger.debug(f"Starting entity extraction for text of length {len(text)}")
            
            # Extract entities using multiple methods
            entities = self._perform_extraction(text)
            
            # Calculate overall confidence
            confidences = [e.confidence for e in entities] if entities else [0.0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            processing_time = (time.time() - start_time) * 1000
            
            logger.info(f"✓ Extracted {len(entities)} entities (confidence: {avg_confidence:.2f})")
            
            return FIREntityExtractionResponse(
                fir_id=fir_id,
                entities=entities,
                entity_count=len(entities),
                extraction_confidence=avg_confidence
            )
            
        except EntityExtractionError:
            raise
        except Exception as e:
            logger.error(f"✗ Entity extraction error: {str(e)}", exc_info=True)
            raise EntityExtractionError(
                message=f"Failed to extract entities: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _perform_extraction(self, text: str) -> List[Entity]:
        """
        Perform entity extraction using multiple strategies
        
        Strategies:
        1. Keyword matching (keyword lists from URDU_KEYWORDS)
        2. Pattern-based extraction (dates, numbers, capitals)
        3. Contextual extraction (words around crime keywords)
        """
        entities = []
        
        # Strategy 1: Keyword-based extraction
        logger.debug("Strategy 1: Keyword-based extraction")
        keyword_entities = self._extract_by_keywords(text)
        entities.extend(keyword_entities)
        
        # Strategy 2: Pattern-based extraction
        logger.debug("Strategy 2: Pattern-based extraction")
        pattern_entities = self._extract_by_patterns(text)
        entities.extend(pattern_entities)
        
        # Strategy 3: Contextual extraction
        logger.debug("Strategy 3: Contextual extraction")
        context_entities = self._extract_by_context(text)
        entities.extend(context_entities)
        
        # Remove duplicates and merge overlapping entities
        entities = self._deduplicate_entities(entities)
        
        logger.debug(f"Total entities extracted: {len(entities)}")
        
        return entities
    
    def _extract_by_keywords(self, text: str) -> List[Entity]:
        """Extract entities by matching against keyword lists"""
        entities = []
        
        for entity_type, keywords_dict in self.URDU_KEYWORDS.items():
            all_keywords = keywords_dict.get('کلیدی الفاظ', []) + keywords_dict.get('انگریزی الفاظ', [])
            
            for keyword in all_keywords:
                pattern = re.compile(re.escape(keyword), re.IGNORECASE | re.UNICODE)
                
                for match in pattern.finditer(text):
                    entity = Entity(
                        text=match.group(),
                        entity_type=entity_type,
                        confidence=0.85,
                        start_pos=match.start(),
                        end_pos=match.end()
                    )
                    entities.append(entity)
        
        logger.debug(f"Keyword-based extraction: {len(entities)} entities")
        return entities
    
    def _extract_by_patterns(self, text: str) -> List[Entity]:
        """Extract entities using regex patterns"""
        entities = []
        
        # Pattern 1: Extract capitalized words (potential names/locations)
        capitalized_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        for match in re.finditer(capitalized_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type="PERSON",
                confidence=0.6,
                start_pos=match.start(),
                end_pos=match.end()
            )
            entities.append(entity)
        
        # Pattern 2: Extract dates (DD/MM/YYYY or YYYY-MM-DD)
        date_pattern = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b|\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b'
        for match in re.finditer(date_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type="TIME",
                confidence=0.95,
                start_pos=match.start(),
                end_pos=match.end()
            )
            entities.append(entity)
        
        # Pattern 3: Extract phone numbers
        phone_pattern = r'\b[+0-9]\d{9,}\b'
        for match in re.finditer(phone_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type="ORGANIZATION",
                confidence=0.7,
                start_pos=match.start(),
                end_pos=match.end()
            )
            entities.append(entity)
        
        logger.debug(f"Pattern-based extraction: {len(entities)} entities")
        return entities
    
    def _extract_by_context(self, text: str) -> List[Entity]:
        """Extract entities by analyzing context around keywords"""
        entities = []
        
        # Find crime-related keywords
        crime_keywords = self.URDU_KEYWORDS['CRIME']['کلیدی الفاظ'] + self.URDU_KEYWORDS['CRIME']['انگریزی الفاظ']
        
        for keyword in crime_keywords:
            pattern = re.compile(r'\w+\s+' + re.escape(keyword) + r'\s+\w+', re.IGNORECASE | re.UNICODE)
            
            for match in re.finditer(pattern, text):
                context = match.group()
                words = context.split()
                
                if len(words) > 0 and words[0].lower() != keyword.lower():
                    entity = Entity(
                        text=words[0],
                        entity_type="PERSON",
                        confidence=0.65,
                        start_pos=match.start(),
                        end_pos=match.start() + len(words[0])
                    )
                    entities.append(entity)
        
        logger.debug(f"Context-based extraction: {len(entities)} entities")
        return entities
    
    def _deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """Remove duplicate or overlapping entities"""
        if not entities:
            return []
        
        entities.sort(key=lambda e: (e.start_pos, -e.confidence))
        
        deduplicated = []
        for entity in entities:
            overlaps = False
            for existing in deduplicated:
                if (entity.start_pos < existing.end_pos and entity.end_pos > existing.start_pos):
                    overlaps = True
                    if entity.confidence > existing.confidence:
                        deduplicated.remove(existing)
                        deduplicated.append(entity)
                    break
            
            if not overlaps:
                deduplicated.append(entity)
        
        return deduplicated


# Global NER service instance
ner_service = NERService()
