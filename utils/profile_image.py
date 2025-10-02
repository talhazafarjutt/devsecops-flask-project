from urllib.request import urlopen, Request
from urllib.parse import urlparse
from mimetypes import guess_type
from base64 import b64encode
import re
import ssl

# Allowed image domains (add more as needed)
ALLOWED_DOMAINS = {
    'example.com',
    'localhost',
    '127.0.0.1',
    'github.io', 
    'example.org'
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
        
        # SECURITY FIX: Only allow HTTP/HTTPS schemes
        if parsed.scheme not in ('http', 'https'):
            return False
            
        # Check if domain is allowed or is localhost for development
        if parsed.hostname not in ALLOWED_DOMAINS:
            # Allow IPv6 localhost
            if parsed.hostname not in ('localhost', '127.0.0.1', '::1', '[::1]'):
                return False
                
        # Check for suspicious patterns
        if re.search(r'[<>"\']', url):
            return False
            
        # Check for IP addresses (only allow localhost)
        if parsed.hostname:
            # SECURITY FIX: Proper exception handling
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', parsed.hostname):
                # IPv4 address - only allow localhost
                if parsed.hostname != '127.0.0.1':
                    return False
                    
        return True
    except Exception:
        return False


def download(url: str) -> bytes:
    """
    Secure URL download with additional validation
    """
    if not is_safe_url(url):
        raise ValueError("Unsafe URL")
    
    # SECURITY FIX: Create secure SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    
    try:
        # SECURITY FIX: Use Request with timeout and User-Agent
        request = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (DevSecOps Scanner)',
            'Accept': 'image/*'
        })
        
        with urlopen(request, timeout=10, context=ssl_context) as response: # nosec B310
            # Verify content type from headers
            content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
            if content_type not in ALLOWED_CONTENT_TYPES:
                raise ValueError("Unsupported content type")
                
            # Limit file size (1MB max)
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > 1024 * 1024:
                raise ValueError("File too large")
                
            # Read with size limit
            data = response.read(1024 * 1024 + 1)  # Read max 1MB + 1 byte
            if len(data) > 1024 * 1024:
                raise ValueError("File too large")
                
            return data
            
    except Exception as e:
        raise ValueError(f"Failed to download image: {str(e)}")


def get_base64_image_blob(url: str) -> str:
    """
    Get base64 encoded image blob with enhanced security
    """
    response = download(url)
    mimetype = guess_type(url)[0] or 'image/png'
    
    # Double-check content type
    if mimetype not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Unsupported image type")
        
    data = b64encode(response).decode('ascii')

    return f"data:{mimetype};base64,{data}"