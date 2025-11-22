
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
        Method representing the business intention to update the author's profile.
        """
        self.name = new_name
        self.description = new_description
        
    # Helper that returns the primitive value for use by the Application layer
    def get_name_value(self) -> str:
        return self.name.value
    
    