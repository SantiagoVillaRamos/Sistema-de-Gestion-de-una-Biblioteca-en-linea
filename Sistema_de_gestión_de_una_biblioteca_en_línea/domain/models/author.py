# c:\...\domain\models\author.py (VERSIÓN MEJORADA)
from dataclasses import dataclass
from domain.models.value_objects.author.author_name import AuthorName  
from domain.models.value_objects.author.author_description import AuthorDescription


@dataclass
class Author:
    
    author_id: str
    name: AuthorName         
    description: AuthorDescription 

    def update_profile(self, new_name: AuthorName, new_description: AuthorDescription) -> None:
        """
        Método que representa la intención de negocio de actualizar el perfil del autor.
        """
        self.name = new_name
        self.description = new_description
        
    #helper que devuelve el valor primitivo para el uso de la capa de Aplicación
    def get_name_value(self) -> str:
        return self.name.value