import re
from typing import List
from domain.models.exceptions.password_validation_error import PasswordValidationError


class PasswordPolicyValidator:
    """
    Password strength validator.
    
    🔒 SECURITY: Enforces strong password requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    
    MIN_LENGTH = 8
    SPECIAL_CHARACTERS = r"[!@#$%^&*(),.?\":{}|<>]"
    
    @classmethod
    def validate(cls, password: str) -> tuple[bool, List[str]]:
        """
        Validate password strength.
        
        Args:
            password: The password to validate
            
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters long")
        
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(cls.SPECIAL_CHARACTERS, password):
            errors.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")
        
        return (len(errors) == 0, errors)
    
    @classmethod
    def validate_or_raise(cls, password: str) -> None:
        """
        Validate password and raise exception if invalid.
        
        Args:
            password: The password to validate
            
        Raises:
            PasswordValidationError: If password doesn't meet requirements
        """
        is_valid, errors = cls.validate(password)
        if not is_valid:
            raise PasswordValidationError("; ".join(errors))
