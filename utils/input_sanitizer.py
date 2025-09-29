import html
import re
from typing import Optional


def sanitize_input(text: Optional[str]) -> Optional[str]:

    if text is None:
        return None
    
    # Remove any null bytes
    text = text.replace('\x00', '')
    
    # Escape HTML characters to prevent XSS
    text = html.escape(text)
    
    # Remove any potential script tags (extra protection)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove any javascript: or vbscript: links
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'vbscript:', '', text, flags=re.IGNORECASE)
    
    return text


def sanitize_email(email: str) -> str:
    """
    Sanitize email input.
    
    Args:
        email: Email to sanitize
        
    Returns:
        Sanitized email
    """
    if email is None:
        return ""
    
    # Remove any null bytes and strip whitespace
    email = email.replace('\x00', '').strip()
    
    # Basic email validation pattern
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    if not email_pattern.match(email):
        raise ValueError("Invalid email format")
    
    return email


def sanitize_text_field(text: str, max_length: int = 1000) -> str:
    """
    Sanitize general text fields.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if text is None:
        return ""
    
    # Remove null bytes and limit length
    text = text.replace('\x00', '')[:max_length]
    
    # Escape HTML
    text = html.escape(text)
    
    return text