from urllib.request import urlopen
from urllib.parse import urlparse
from mimetypes import guess_type
from base64 import b64encode
import re

# Allowed image domains (add more as needed)
ALLOWED_DOMAINS = {
    'example.com',
    'localhost',
    '127.0.0.1'
}

# Allowed image content types
ALLOWED_CONTENT_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp'
}


def is_safe_url(url: str) -> bool:
    """
    Check if URL is safe to download from.
    
    Args:
        url: URL to check
        
    Returns:
        True if URL is safe, False otherwise
    """
    try:
        parsed = urlparse(url)
        
        # Check if scheme is HTTP or HTTPS
        if parsed.scheme not in ('http', 'https'):
            return False
            
        # Check if domain is allowed
        if parsed.hostname not in ALLOWED_DOMAINS:
            # For localhost development, allow localhost and 127.0.0.1
            if parsed.hostname not in ('localhost', '127.0.0.1'):
                return False
                
        # Check for suspicious patterns
        if re.search(r'[<>"\']', url):
            return False
            
        return True
    except Exception:
        return False


def download(url: str) -> bytes:
    if not is_safe_url(url):
        raise ValueError("Unsafe URL")
        
    with urlopen(url) as response:
        # Check content type
        content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("Unsupported content type")
            
        # Limit file size (1MB max)
        if int(response.headers.get('Content-Length', 0)) > 1024 * 1024:
            raise ValueError("File too large")
            
        return response.read()


def get_base64_image_blob(url: str) -> str:
    response = download(url)
    mimetype = guess_type(url)[0] or 'image/png'
    
    # Double-check content type
    if mimetype not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Unsupported image type")
        
    data = b64encode(response).decode('ascii')

    return f"data:{mimetype};base64,{data}"
