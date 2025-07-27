"""
Utility functions for the hiring assistant
"""

import re
from typing import Dict, List, Optional

class DataValidator:
    """Validate and clean user input data"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if email format is valid"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Check if phone number format is reasonable"""
        # Remove all non-digits
        digits_only = re.sub(r'\D', '', phone)
        # Check if it's between 10-15 digits (international format)
        return 10 <= len(digits_only) <= 15
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text input"""
        if not text:
            return ""
        return text.strip().replace('\n', ' ').replace('\r', '')

class TechStackExtractor:
    """Extract and categorize technical skills"""
    
    PROGRAMMING_LANGUAGES = [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 
        'swift', 'kotlin', 'go', 'rust', 'typescript', 'r', 'scala'
    ]
    
    FRAMEWORKS = [
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'rails',
        'express', 'next.js', 'nuxt', 'laravel', 'asp.net'
    ]
    
    DATABASES = [
        'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
        'cassandra', 'elasticsearch'
    ]
    
    @classmethod
    def extract_skills(cls, text: str) -> Dict[str, List[str]]:
        """Extract categorized skills from text"""
        text_lower = text.lower()
        
        found_languages = [lang for lang in cls.PROGRAMMING_LANGUAGES 
                          if lang in text_lower]
        found_frameworks = [fw for fw in cls.FRAMEWORKS 
                           if fw in text_lower]
        found_databases = [db for db in cls.DATABASES 
                          if db in text_lower]
        
        return {
            'languages': found_languages,
            'frameworks': found_frameworks,
            'databases': found_databases
        }
