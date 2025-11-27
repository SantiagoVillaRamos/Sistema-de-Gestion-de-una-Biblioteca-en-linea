"""
Input validation and sanitization utilities for security.

This module provides functions to validate and sanitize user inputs
to prevent XSS, SQL injection, and other injection attacks.
"""

import re
import html
from typing import Optional


class InputValidationError(Exception):
    """Raised when input validation fails for security reasons."""
    pass


def sanitize_html(text: str) -> str:
    """
    Sanitize HTML by escaping special characters.
    
    Converts HTML special characters to their entity equivalents
    to prevent XSS attacks.
    
    Args:
        text: Input text that may contain HTML
        
    Returns:
        Sanitized text with HTML entities escaped
        
    Example:
        >>> sanitize_html("<script>alert('XSS')</script>")
        "&lt;script&gt;alert('XSS')&lt;/script&gt;"
    """
    if not text:
        return text
    return html.escape(text, quote=True)


def strip_html_tags(text: str) -> str:
    """
    Remove all HTML tags from text.
    
    Args:
        text: Input text that may contain HTML tags
        
    Returns:
        Text with all HTML tags removed
        
    Example:
        >>> strip_html_tags("<p>Hello <b>World</b></p>")
        "Hello World"
    """
    if not text:
        return text
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    clean_text = html.unescape(clean_text)
    return clean_text.strip()


def validate_safe_text(text: str, field_name: str = "field") -> str:
    """
    Validate that text contains only safe characters for names and titles.
    
    Allows: letters (any language), numbers, spaces, hyphens, apostrophes, periods, commas
    Blocks: HTML tags, SQL keywords, special characters
    
    Args:
        text: Text to validate
        field_name: Name of the field for error messages
        
    Returns:
        Sanitized text if valid
        
    Raises:
        InputValidationError: If text contains unsafe characters
    """
    if not text:
        return text
    
    # Strip HTML tags first
    clean_text = strip_html_tags(text)
    
    # 🔒 SECURITY: Reject if HTML tags were present (strict validation)
    if clean_text != text:
        raise InputValidationError(f"{field_name} contains HTML tags or encoded entities")
    
    # Check for SQL injection keywords (case-insensitive)
    sql_keywords = [
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'EXEC', 'EXECUTE', 'UNION', 'DECLARE', 'CAST', 'CONVERT', '--', ';--'
    ]
    
    text_upper = clean_text.upper()
    for keyword in sql_keywords:
        if keyword in text_upper:
            raise InputValidationError(
                f"{field_name} contains potentially dangerous content: '{keyword}'"
            )
    
    # Check for dangerous special characters
    dangerous_chars = ['<', '>', '{', '}', '\\', '|', '^', '~', '`']
    for char in dangerous_chars:
        if char in clean_text:
            raise InputValidationError(
                f"{field_name} contains invalid character: '{char}'"
            )
    
    return clean_text


def validate_isbn(isbn: str) -> str:
    """
    Validate ISBN-10 or ISBN-13 format.
    
    Args:
        isbn: ISBN string to validate
        
    Returns:
        Cleaned ISBN (digits and hyphens only)
        
    Raises:
        InputValidationError: If ISBN format is invalid
        
    Example:
        >>> validate_isbn("978-0-452-28423-4")
        "978-0-452-28423-4"
        >>> validate_isbn("0-452-28423-4")
        "0-452-28423-4"
    """
    if not isbn:
        raise InputValidationError("ISBN cannot be empty")
    
    # Remove spaces and convert to uppercase
    clean_isbn = isbn.replace(' ', '').replace('-', '').upper()
    
    # Check if it contains only digits and X (for ISBN-10)
    if not re.match(r'^[\dX]+$', clean_isbn):
        raise InputValidationError("ISBN must contain only digits and hyphens")
    
    # Validate length (10 for ISBN-10, 13 for ISBN-13)
    if len(clean_isbn) not in [10, 13]:
        raise InputValidationError(
            f"ISBN must be 10 or 13 digits, got {len(clean_isbn)}"
        )
    
    # Return original format (with hyphens)
    return isbn.strip()


def validate_no_sql_keywords(text: str, field_name: str = "field") -> str:
    """
    Check for SQL injection keywords in text.
    
    Args:
        text: Text to validate
        field_name: Name of the field for error messages
        
    Returns:
        Original text if valid
        
    Raises:
        InputValidationError: If SQL keywords are detected
    """
    if not text:
        return text
    
    sql_patterns = [
        r'\bSELECT\b', r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b',
        r'\bDROP\b', r'\bCREATE\b', r'\bALTER\b', r'\bEXEC\b',
        r'\bUNION\b', r'\bDECLARE\b', r'--', r';--', r'/\*', r'\*/'
    ]
    
    text_upper = text.upper()
    for pattern in sql_patterns:
        if re.search(pattern, text_upper):
            raise InputValidationError(
                f"{field_name} contains potentially dangerous SQL pattern"
            )
    
    return text


def validate_description(text: str, max_length: int = 2000) -> str:
    """
    Validate and sanitize description text.
    
    Removes HTML tags and validates length.
    
    Args:
        text: Description text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized description
        
    Raises:
        InputValidationError: If description is too long
    """
    if not text:
        return text
    
    # Strip HTML tags
    clean_text = strip_html_tags(text)
    
    if len(clean_text) > max_length:
        raise InputValidationError(
            f"Description too long: {len(clean_text)} characters (max {max_length})"
        )
    
    return clean_text


def validate_name(name: str, min_length: int = 2, max_length: int = 100) -> str:
    """
    Validate person or entity name.
    
    Args:
        name: Name to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        Validated name
        
    Raises:
        InputValidationError: If name is invalid
    """
    if not name or not name.strip():
        raise InputValidationError("Name cannot be empty")
    
    clean_name = validate_safe_text(name.strip(), "Name")
    
    if len(clean_name) < min_length:
        raise InputValidationError(
            f"Name too short: {len(clean_name)} characters (min {min_length})"
        )
    
    if len(clean_name) > max_length:
        raise InputValidationError(
            f"Name too long: {len(clean_name)} characters (max {max_length})"
        )
    
    return clean_name
