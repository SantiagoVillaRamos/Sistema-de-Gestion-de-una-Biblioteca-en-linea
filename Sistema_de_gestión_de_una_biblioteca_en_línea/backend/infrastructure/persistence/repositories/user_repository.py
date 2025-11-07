from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime

# Importaciones de Infraestructura
from infrastructure.persistence.models import UserModel

# Importaciones de Dominio (Puertos y Entidades)
from domain.ports.user_repository import UserRepository

from domain.models.author import Author
from domain.models.book import Book
from domain.models.user import User
from domain.models.loan import Loan
# Asumo que estos están en domain.models...
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.value_objects.due_date import DueDate
from domain.models.exceptions.business_exception import BusinessNotFoundError 



# --- REPOSITORIO DE USUARIO (Ejemplo Simplificado) ---
class SQLAlchemyUserRepository(UserRepository): # CORREGIDO: Hereda del Puerto
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _map_to_domain(self, db_user: UserModel) -> Optional[User]:
        if not db_user:
            return None
        # Mapeo usando los Objetos de Valor del Dominio
        return User(
            user_id=db_user.id,
            name=db_user.name,
            email=Email(db_user.email),
            password=Password(db_user.password_hash), # Asumo que Password maneja el hash internamente 
            user_type=db_user.user_type,
            roles=db_user.roles.split(",") if db_user.roles else [],
            is_active=db_user.is_active
        )

    async def save(self, user: User) -> None: # CORREGIDO: Async (Usado para crear/actualizar)
        db_user = await self.session.get(UserModel, user.user_id)
        
        if db_user:
            # Actualización
            db_user.name = user.name
            db_user.email = str(user.email)
            db_user.password_hash = str(user.password) # El Agregado User debe proveer el HASH aquí
            db_user.user_type = user.user_type
            db_user.roles = ",".join(user.roles)
            db_user.is_active = user.is_active
        else:
            # Creación
            db_user = UserModel(
                id=user.user_id,
                name=user.name,
                email=str(user.email),
                password_hash=str(user.password),
                user_type=user.user_type,
                roles=",".join(user.roles),
                is_active=user.is_active
            )
            self.session.add(db_user)
            
        try:
            await self.session.commit()
            # No hay refresh asíncrono simple en esta API, pero el objeto User ya está completo.
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def find_by_id(self, user_id: str) -> Optional[User]:
        db_user = await self.session.get(UserModel, user_id)
        return await self._map_to_domain(db_user)

    async def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self.session.execute(stmt)
        db_user = result.scalars().first()
        return await self._map_to_domain(db_user)

    # Implementación de otros métodos del Puerto (find_all, delete, find_by_ids...)
    async def find_all(self) -> list[User]:
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [await self._map_to_domain(u) for u in db_users]

    async def delete(self, user: User) -> None:
        stmt = delete(UserModel).where(UserModel.id == user.user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_by_ids(self, user_ids: list[str]) -> list[User]:
        stmt = select(UserModel).where(UserModel.id.in_(user_ids))
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [await self._map_to_domain(u) for u in db_users]