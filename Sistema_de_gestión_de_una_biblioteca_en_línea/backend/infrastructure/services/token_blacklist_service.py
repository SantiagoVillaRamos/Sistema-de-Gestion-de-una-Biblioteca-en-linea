from typing import Set
from datetime import datetime, timedelta
import threading


class TokenBlacklistService:
    """
    In-memory token blacklist service.
    
    🔒 SECURITY: Tracks revoked tokens to prevent reuse after logout.
    
    Note: In production, use Redis or a database for persistence
    and distributed systems support.
    """
    
    def __init__(self):
        self._blacklist: Set[str] = set()
        self._lock = threading.Lock()
        # Store token expiration times to clean up old entries
        self._token_expiry: dict[str, datetime] = {}
    
    def add_token(self, token: str, expires_at: datetime) -> None:
        """
        Add a token to the blacklist.
        
        Args:
            token: The JWT token to blacklist
            expires_at: When the token naturally expires
        """
        with self._lock:
            self._blacklist.add(token)
            self._token_expiry[token] = expires_at
    
    def is_blacklisted(self, token: str) -> bool:
        """
        Check if a token is blacklisted.
        
        Args:
            token: The JWT token to check
            
        Returns:
            bool: True if token is blacklisted, False otherwise
        """
        with self._lock:
            return token in self._blacklist
    
    def cleanup_expired(self) -> int:
        """
        Remove expired tokens from the blacklist.
        
        🔒 SECURITY: Prevents memory bloat by removing old entries.
        
        Returns:
            int: Number of tokens removed
        """
        now = datetime.utcnow()
        removed_count = 0
        
        with self._lock:
            expired_tokens = [
                token for token, expiry in self._token_expiry.items()
                if expiry < now
            ]
            
            for token in expired_tokens:
                self._blacklist.discard(token)
                del self._token_expiry[token]
                removed_count += 1
        
        return removed_count
    
    def get_blacklist_size(self) -> int:
        """Get the current size of the blacklist."""
        with self._lock:
            return len(self._blacklist)
