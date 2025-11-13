from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from infrastructure.persistence.models import UserModel
from domain.ports.user_repository import UserRepository
from domain.models.user import User
from domain.models.exceptions.business_exception import BusinessError 
from infrastructure.mapper_infrastructure.user_mapper import UserMapper



# --- REPOSITORIO DE USUARIO ---
class SQLAlchemyUserRepository(UserRepository):
    """
    Adaptador de Infraestructura que implementa el Puerto UserRepository
    utilizando SQLAlchemy ORM.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None: 
        db_user = await self.session.get(UserModel, user.user_id)
        
        db_user_mapper = UserMapper.to_db_model(user, db_user)
        
        if not await self.session.get(UserModel, user.user_id):
            self.session.add(db_user_mapper)
            
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise BusinessError(f"Error: - {e}")


    async def find_by_id(self, user_id: str) -> Optional[User]:
        db_user = await self.session.get(UserModel, user_id)
        return UserMapper.to_domain(db_user)


    async def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()
        return UserMapper.to_domain(db_user)


    async def find_all(self) -> list[User]:
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [UserMapper.to_domain(u) for u in db_users]


    async def delete(self, user: User) -> None:
        stmt = delete(UserModel).where(UserModel.id == user.user_id)
        await self.session.execute(stmt)
        await self.session.commit()


    async def find_by_ids(self, user_ids: list[str]) -> list[User]:
        stmt = select(UserModel).where(UserModel.id.in_(user_ids))
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [UserMapper.to_domain(u) for u in db_users]
    
    