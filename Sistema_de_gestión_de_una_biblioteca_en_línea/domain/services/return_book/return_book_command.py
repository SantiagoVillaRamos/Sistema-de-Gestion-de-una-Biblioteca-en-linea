from dataclasses import dataclass

@dataclass(frozen=True)
class ReturnBookCommand:
    """
    DTO para los datos de entrada del caso de uso de devolver un libro.
    """
    loan_id: str
    
@dataclass(frozen=True)
class MessageResponse:
    """
    DTO para la respuesta del caso de uso de devolver un libro.
    """
    message: str