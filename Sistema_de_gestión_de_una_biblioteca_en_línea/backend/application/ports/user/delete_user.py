from abc import ABC, abstractmethod


class DeleteUser(ABC):
    
    @abstractmethod
    async def delete(self, user_id: str) -> None:
        pass
