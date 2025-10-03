from typing import Dict, Optional
from application.ports.user_repository import UserRepository
from domain.entities.user import User

from domain.exceptions.user import UserAlreadyExistsError, UserNotFoundError

class UserInMemoryRepository(UserRepository):
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        print(f"\nDiccionario:{self._users}\n")
        
    async def save(self, user: User) -> None:
        user_exists = any(b for b in self._users.values() if b.email == user.email)
        if user_exists:
            raise UserAlreadyExistsError(user.email)
        self._users[user.user_id] = user

    async def find_by_id(self, user_id: str) -> Optional[User]:
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundError(user_id, "Usuario no encontrado")
        return user
        