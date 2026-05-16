"""
Urdu Text Preprocessing Service
Handles text cleaning, normalization, and tokenization for Urdu FIRs

Issue #2: Urdu text preprocessing
"""

import logging
import re
import unicodedata
import time
from typing import Dict, Any, List
from app.models.schemas import FIRPreprocessResponse
from app.core.errors import PreprocessingError

logger = logging.getLogger(__name__)

# Urdu Unicode ranges
URDU_START = 0x0600
URDU_END = 0x06FF


class PreprocessingService:
    """
    Service for preprocessing Urdu FIR text
    Handles cleaning, normalization, tokenization, and language detection
    """
    
    # Urdu-specific character mappings for normalization
    URDU_CHAR_MAPPING = {
        '\u0643': '\u06a9',  # Arabic Kaf to Urdu Kaf
        '\u064a': '\u06cc',  # Arabic Yaa to Urdu Yaa
    }
    
    # Common Urdu stop words
    URDU_STOP_WORDS = {
        'کہ', 'ہے', 'اور', 'یہ', 'کیا', 'کے', 'کو', 'میں', 'نے',
        'یا', 'ہو', 'سے', 'تک', 'ان', 'تھا', 'اس', 'ہوں'
    }
    
    def __init__(self):
        """Initialize preprocessing service"""
        logger.info("✓ Initializing PreprocessingService")
    
    def preprocess(self, text: str, fir_id: str = None) -> FIRPreprocessResponse:
        """
        Preprocess Urdu FIR text with complete pipeline
        
        Args:
            text: Raw Urdu FIR text
            fir_id: Optional FIR identifier
            
        Returns:
            FIRPreprocessResponse with preprocessed text and metadata
            
        Raises:
            PreprocessingError: If preprocessing fails
        """
        start_time = time.time()
        
        try:
            if not text or len(text.strip()) == 0:
                raise PreprocessingError("FIR text cannot be empty")
            
            # Step 1: Text cleaning
            logger.debug("Step 1: Cleaning text")
            cleaned_text = self._clean_text(text)
            
            # Step 2: Unicode normalization
            logger.debug("Step 2: Normalizing unicode")
            normalized_text = self._normalize_unicode(cleaned_text)
            
            # Step 3: Urdu-specific normalization
            logger.debug("Step 3: Applying Urdu normalization")
            urdu_normalized = self._normalize_urdu_characters(normalized_text)
            
            # Step 4: Remove extra whitespace
            logger.debug("Step 4: Removing extra whitespace")
            final_text = self._remove_extra_whitespace(urdu_normalized)
            
            # Step 5: Tokenization
            logger.debug("Step 5: Tokenizing text")
            tokens = self._tokenize(final_text)
            
            # Step 6: Language detection
            logger.debug("Step 6: Detecting language")
            language = self._detect_language(final_text)
            
            processing_time = (time.time() - start_time) * 1000
            
            logger.info(f"✓ Successfully preprocessed text (length: {len(final_text)}, tokens: {len(tokens)})")
            
            return FIRPreprocessResponse(
                original_text=text,
                preprocessed_text=final_text,
                text_length=len(final_text),
                token_count=len(tokens),
                language_detected=language
            )
            
        except PreprocessingError:
            raise
        except Exception as e:
            logger.error(f"✗ Preprocessing error: {str(e)}", exc_info=True)
            raise PreprocessingError(
                message=f"Failed to preprocess text: {str(e)}",
                details={"error_type": type(e).__name__}
            )
    
    def _clean_text(self, text: str) -> str:
        """Remove unnecessary characters and formatting issues"""
        if not text:
            return text
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),])+', '', text)
        
        # Remove email addresses
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\+?[0-9][0-9\s\-\(\)]{8,}', '', text)
        
        # Remove mentions and hashtags
        text = re.sub(r'[@#][\w]+', '', text)
        
        # Remove extra punctuation
        text = re.sub(r'[.!?]{2,}', '.', text)
        
        # Remove control characters
        text = ''.join(char for char in text if not unicodedata.category(char).startswith('C'))
        
        return text.strip()
    
    def _normalize_unicode(self, text: str) -> str:
        """Apply Unicode normalization (NFC)"""
        if not text:
            return text
        
        normalized = unicodedata.normalize('NFC', text)
        return normalized
    
    def _normalize_urdu_characters(self, text: str) -> str:
        """Apply Urdu-specific character normalization"""
        if not text:
            return text
        
        normalized = text
        
        # Apply character mappings
        for arabic_char, urdu_char in self.URDU_CHAR_MAPPING.items():
            normalized = normalized.replace(arabic_char, urdu_char)
        
        # Normalize digits
        normalized = self._normalize_digits(normalized)
        
        # Normalize hamza
        normalized = self._normalize_hamza(normalized)
        
        return normalized
    
    def _normalize_digits(self, text: str) -> str:
        """Normalize different digit representations to ASCII"""
        if not text:
            return text
        
        # Arabic-Indic digits
        arabic_indic = '٠١٢٣٤٥٦٧٨٩'
        # Extended Arabic-Indic (Urdu)
        extended = '۰۱۲۳۴۵۶۷۸۹'
        ascii_digits = '0123456789'
        
        for i, digit in enumerate(ascii_digits):
            text = text.replace(arabic_indic[i], digit)
            text = text.replace(extended[i], digit)
        
        return text
    
    def _normalize_hamza(self, text: str) -> str:
        """Normalize various Hamza forms"""
        if not text:
            return text
        
        text = text.replace('\u0621', '')  # Remove Hamza
        text = text.replace('\u0623', '\u0627')  # Hamza on Alif -> Alif
        text = text.replace('\u0625', '\u0627')  # Hamza below Alif -> Alif
        text = text.replace('\u0624', '\u0648')  # Hamza on Waw -> Waw
        
        return text
    
    def _remove_extra_whitespace(self, text: str) -> str:
        """Remove extra whitespace"""
        if not text:
            return text
        
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize Urdu text into words"""
        if not text:
            return []
        
        # Split by whitespace
        tokens = text.split()
        
        # Process tokens to separate attached punctuation
        processed_tokens = []
        for token in tokens:
            if token:
                processed_tokens.append(token)
        
        return processed_tokens
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        if not text:
            return 'unknown'
        
        urdu_count = 0
        total_chars = 0
        
        for char in text:
            code_point = ord(char)
            
            if URDU_START <= code_point <= URDU_END:
                urdu_count += 1
            
            if unicodedata.category(char)[0] in ('L', 'M', 'N'):
                total_chars += 1
        
        if total_chars == 0:
            return 'unknown'
        
        urdu_percentage = (urdu_count / total_chars) * 100
        
        if urdu_percentage > 80:
            return 'urdu'
        elif urdu_percentage > 30:
            return 'mixed'
        else:
            return 'english'


# Global preprocessing service instance
preprocessing_service = PreprocessingService()
