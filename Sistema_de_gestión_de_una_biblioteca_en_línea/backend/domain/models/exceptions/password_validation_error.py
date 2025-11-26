"""
Password validation exception.

This exception is raised when a password does not meet the security requirements.
"""


class PasswordValidationError(Exception):
    """
    Exception raised when password validation fails.
    
    This exception should be raised when a password does not meet
    the required security policy (length, complexity, etc.).
    
    Attributes:
        message: Detailed error message describing which requirements were not met
    """
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
