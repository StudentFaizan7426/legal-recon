"""
Timeline Generation Service
Reconstructs chronological sequence of events from Urdu FIR text

Issue #5: Timeline generation
"""

import logging
import re
import time
from typing import List, Optional
from datetime import datetime
from app.models.schemas import TimelineEvent, TimelineGenerationResponse, Entity
from app.core.errors import TimelineGenerationError

logger = logging.getLogger(__name__)


class TimelineService:
    """
    Service for generating event timelines from FIR text
    Extracts and sequences events chronologically
    """
    
    # Temporal indicators for event extraction
    TEMPORAL_INDICATORS = {
        'absolute': {
            'urdu': ['جنوری', 'فروری', 'مارچ', 'اپریل', 'مئی', 'جون', 'جولائی', 'اگست', 'ستمبر', 'اکتوبر', 'نومبر', 'دسمبر'],
            'english': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        },
        'relative': {
            'urdu': ['پہلے', 'پچھلے', 'اگلے', 'کل', 'آج', 'رات', 'دن', 'صبح', 'شام'],
            'english': ['before', 'after', 'last', 'next', 'yesterday', 'today', 'night', 'day', 'morning', 'evening']
        },
        'action_verbs': {
            'urdu': ['کیا', 'کرتے', 'جب', 'تب', 'پھر', 'اسی طرح'],
            'english': ['did', 'then', 'after', 'before', 'when', 'while', 'next', 'later']
        }
    }
    
    def __init__(self):
        """Initialize timeline service"""
        logger.info("✓ Initializing TimelineService")
    
    def generate_timeline(self, text: str, entities: List[Entity] = None, fir_id: str = None) -> TimelineGenerationResponse:
        """
        Generate timeline from FIR text
        
        Extracts temporal expressions, events, and their sequence
        
        Args:
            text: FIR text
            entities: Extracted entities (optional)
            fir_id: FIR identifier
            
        Returns:
            TimelineGenerationResponse with event timeline
            
        Raises:
            TimelineGenerationError: If generation fails
        """
        start_time = time.time()
        
        try:
            if not text or len(text.strip()) == 0:
                raise TimelineGenerationError("FIR text cannot be empty")
            
            logger.debug(f"Starting timeline generation for text of length {len(text)}")
            
            # Extract temporal expressions and events
            events = self._extract_events(text, entities)
            
            # Sort events chronologically
            events = self._sort_chronologically(events)
            
            # Extract event sequence
            event_ids = [e.event_id for e in events]
            
            # Calculate timeline coverage
            timestamps = [e.timestamp for e in events if e.timestamp]
            temporal_coverage_days = None
            if len(timestamps) >= 2:
                try:
                    temporal_coverage_days = (max(timestamps) - min(timestamps)).days
                except (TypeError, AttributeError):
                    temporal_coverage_days = None
            
            # Calculate overall confidence
            confidences = [e.confidence for e in events] if events else [0.0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            processing_time = (time.time() - start_time) * 1000
            
            logger.info(f"✓ Generated timeline with {len(events)} events")
            
            return TimelineGenerationResponse(
                fir_id=fir_id,
                timeline_events=events,
                event_sequence=event_ids,
                start_event=event_ids[0] if event_ids else None,
                end_event=event_ids[-1] if event_ids else None,
                temporal_coverage_days=temporal_coverage_days,
                reconstruction_confidence=avg_confidence
            )
            
        except TimelineGenerationError:
            raise
        except Exception as e:
            logger.error(f"✗ Timeline generation error: {str(e)}", exc_info=True)
            raise TimelineGenerationError(
                message=f"Failed to generate timeline: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _extract_events(self, text: str, entities: List[Entity] = None) -> List[TimelineEvent]:
        """
        Extract events from FIR text
        
        Strategies:
        1. Temporal expression extraction
        2. Sentence-based event extraction
        3. Action verb identification
        """
        events = []
        event_id_counter = 1
        
        # Split text into sentences
        sentences = re.split(r'[.!?؟۔]+', text)
        
        for sent_idx, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Extract temporal information
            temporal_info = self._extract_temporal_info(sentence)
            
            # Extract location from entities if available
            location = None
            if entities:
                for entity in entities:
                    if entity.entity_type == "LOCATION":
                        location = entity.text
                        break
            
            # Extract entities involved in this sentence
            entities_involved = []
            if entities:
                for entity in entities:
                    if entity.text.lower() in sentence.lower():
                        entities_involved.append(entity.text)
            
            # Create event if sentence contains temporal or action information
            if temporal_info or entities_involved or len(sentence) > 20:
                event = TimelineEvent(
                    event_id=f"event_{event_id_counter}",
                    event_description=sentence,
                    timestamp=temporal_info.get('timestamp') if temporal_info else None,
                    location=location,
                    entities_involved=entities_involved,
                    confidence=temporal_info.get('confidence', 0.6) if temporal_info else 0.5,
                    source_text_span=sentence[:100]
                )
                events.append(event)
                event_id_counter += 1
        
        logger.debug(f"Extracted {len(events)} events from {len(sentences)} sentences")
        return events
    
    def _extract_temporal_info(self, sentence: str) -> Optional[dict]:
        """Extract temporal information from a sentence"""
        temporal_info = {}
        
        # Look for date patterns (DD/MM/YYYY, DD-MM-YYYY, etc.)
        date_pattern = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
        date_match = re.search(date_pattern, sentence)
        
        if date_match:
            try:
                day, month, year = date_match.groups()
                if len(year) == 2:
                    year = "20" + year
                
                timestamp = datetime(int(year), int(month), int(day))
                temporal_info['timestamp'] = timestamp
                temporal_info['confidence'] = 0.95
                return temporal_info
            except (ValueError, TypeError):
                logger.debug(f"Could not parse date: {date_match.group()}")
        
        # Look for month names (Urdu or English)
        all_months = self.TEMPORAL_INDICATORS['absolute']['urdu'] + self.TEMPORAL_INDICATORS['absolute']['english']
        for idx, month_name in enumerate(all_months):
            if month_name.lower() in sentence.lower():
                year_pattern = r'\b(20\d{2}|19\d{2})\b'
                year_match = re.search(year_pattern, sentence)
                
                if year_match:
                    try:
                        month_num = (idx % 12) + 1
                        timestamp = datetime(int(year_match.group()), month_num, 1)
                        temporal_info['timestamp'] = timestamp
                        temporal_info['confidence'] = 0.8
                        return temporal_info
                    except ValueError:
                        pass
        
        # Look for relative temporal indicators
        relative_terms = self.TEMPORAL_INDICATORS['relative']['urdu'] + self.TEMPORAL_INDICATORS['relative']['english']
        for term in relative_terms:
            if term.lower() in sentence.lower():
                temporal_info['confidence'] = 0.4
                return temporal_info
        
        return None
    
    def _sort_chronologically(self, events: List[TimelineEvent]) -> List[TimelineEvent]:
        """Sort events in chronological order"""
        # Separate events with and without timestamps
        timestamped = [e for e in events if e.timestamp]
        non_timestamped = [e for e in events if not e.timestamp]
        
        # Sort timestamped events chronologically
        timestamped.sort(key=lambda e: e.timestamp)
        
        # Combine: timestamped first, then non-timestamped in original order
        sorted_events = timestamped + non_timestamped
        
        logger.debug(f"Sorted {len(timestamped)} timestamped and {len(non_timestamped)} non-timestamped events")
        return sorted_events


# Global timeline service instance
timeline_service = TimelineService()
