import logging
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import json


# Configure security logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# Create file handler for security events
security_handler = logging.FileHandler('security_audit.log')
security_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
security_handler.setFormatter(formatter)
security_logger.addHandler(security_handler)

# Also log to console in development
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
security_logger.addHandler(console_handler)


class SecurityLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log security-relevant events.
    
    🔒 SECURITY: Logs all authentication and authorization events for audit trail.
    
    Logged Events:
    - Authentication attempts (login, refresh, logout)
    - Authorization failures (403)
    - Authentication failures (401)
    - Suspicious activity patterns
    """
    
    # Endpoints to monitor
    AUTH_ENDPOINTS = ['/auth/login', '/auth/refresh', '/auth/logout']
    PROTECTED_ENDPOINTS_PREFIXES = ['/users', '/library', '/books', '/authors']
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log security events."""
        
        start_time = time.time()
        path = request.url.path
        method = request.method
        client_ip = request.client.host if request.client else "unknown"
        
        # Get authorization header
        auth_header = request.headers.get("authorization", "")
        has_token = bool(auth_header and auth_header.startswith("Bearer "))
        
        # Process request
        response = await call_next(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        status_code = response.status_code
        
        # Log security-relevant events
        self._log_security_event(
            path=path,
            method=method,
            status_code=status_code,
            client_ip=client_ip,
            has_token=has_token,
            duration=duration
        )
        
        return response
    
    def _log_security_event(
        self,
        path: str,
        method: str,
        status_code: int,
        client_ip: str,
        has_token: bool,
        duration: float
    ):
        """Log security event with appropriate level."""
        
        event_data = {
            "path": path,
            "method": method,
            "status": status_code,
            "ip": client_ip,
            "has_token": has_token,
            "duration_ms": round(duration * 1000, 2)
        }
        
        # Authentication endpoints
        if path in self.AUTH_ENDPOINTS:
            if path == '/auth/login':
                if status_code == 200:
                    security_logger.info(f"✅ LOGIN SUCCESS - {json.dumps(event_data)}")
                elif status_code == 429:
                    security_logger.warning(f"⚠️  RATE LIMIT EXCEEDED - {json.dumps(event_data)}")
                else:
                    security_logger.warning(f"❌ LOGIN FAILED - {json.dumps(event_data)}")
            
            elif path == '/auth/refresh':
                if status_code == 200:
                    security_logger.info(f"🔄 TOKEN REFRESHED - {json.dumps(event_data)}")
                else:
                    security_logger.warning(f"❌ REFRESH FAILED - {json.dumps(event_data)}")
            
            elif path == '/auth/logout':
                if status_code == 200:
                    security_logger.info(f"👋 LOGOUT SUCCESS - {json.dumps(event_data)}")
                else:
                    security_logger.warning(f"❌ LOGOUT FAILED - {json.dumps(event_data)}")
        
        # Authorization failures
        elif status_code == 403:
            security_logger.warning(f"🚫 AUTHORIZATION DENIED - {json.dumps(event_data)}")
        
        # Authentication failures on protected endpoints
        elif status_code == 401 and self._is_protected_endpoint(path):
            security_logger.warning(f"🔒 AUTHENTICATION REQUIRED - {json.dumps(event_data)}")
        
        # Suspicious: Accessing protected endpoint without token
        elif not has_token and self._is_protected_endpoint(path) and method != "GET":
            security_logger.warning(f"⚠️  SUSPICIOUS: No token on protected endpoint - {json.dumps(event_data)}")
    
    def _is_protected_endpoint(self, path: str) -> bool:
        """Check if endpoint is protected."""
        return any(path.startswith(prefix) for prefix in self.PROTECTED_ENDPOINTS_PREFIXES)


def log_security_event(event_type: str, details: dict):
    """
    Helper function to log custom security events.
    
    Usage:
        log_security_event("PASSWORD_CHANGE", {
            "user_id": user.user_id,
            "success": True
        })
    """
    security_logger.info(f"{event_type} - {json.dumps(details)}")
