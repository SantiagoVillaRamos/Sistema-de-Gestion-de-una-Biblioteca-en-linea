'''Seed script to populate the database with initial data.
Run this after applying migrations with: python seed_data.py
'''

from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.models import UserModel, BookModel, AuthorModel
import uuid
import bcrypt
import os

# 🔒 SECURITY: Load seed passwords from environment
SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "Admin@1234")
SEED_USER_PASSWORD = os.getenv("SEED_USER_PASSWORD", "Password123!")

# Warn if using defaults
if SEED_ADMIN_PASSWORD == "Admin@1234":
    print("⚠️  WARNING: Using default admin password. Set SEED_ADMIN_PASSWORD in .env")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed_data():
    db = SessionLocal()
    try:
        # Create admin user (strong password meets policy)
        admin_user = UserModel(
            id=str(uuid.uuid4()),
            name="Admin User",
            email="admin@library.com",
            password_hash=hash_password(SEED_ADMIN_PASSWORD),
            user_type="premium",
            roles="ADMIN,MEMBER",
            is_active=True,
        )
        db.add(admin_user)

        # Create regular users with strong passwords
        user1 = UserModel(
            id=str(uuid.uuid4()),
            name="John Doe",
            email="john@example.com",
            password_hash=hash_password(SEED_USER_PASSWORD),
            user_type="general",
            roles="MEMBER",
            is_active=True,
        )
        db.add(user1)

        user2 = UserModel(
            id=str(uuid.uuid4()),
            name="Jane Smith",
            email="jane@example.com",
            password_hash=hash_password(SEED_USER_PASSWORD),
            user_type="premium",
            roles="MEMBER",
            is_active=True,
        )
        db.add(user2)

        # Create authors
        author1 = AuthorModel(
            id=str(uuid.uuid4()),
            name="Gabriel García Márquez",
            description="Nobel Prize winner, known for One Hundred Years of Solitude."
        )
        db.add(author1)

        author2 = AuthorModel(
            id=str(uuid.uuid4()),
            name="J.K. Rowling",
            description="Author of the Harry Potter series."
        )
        db.add(author2)

        # Create books
        book1 = BookModel(
            id=str(uuid.uuid4()),
            title="One Hundred Years of Solitude",
            description="A landmark novel of magical realism.",
            isbn="978-0060883287",
            available_copies=5
        )
        # Add author relationship (assuming many-to-many or similar)
        book1.authors.append(author1)
        db.add(book1)

        book2 = BookModel(
            id=str(uuid.uuid4()),
            title="Harry Potter and the Sorcerer's Stone",
            description="The first book in the Harry Potter series.",
            isbn="978-0590353427",
            available_copies=10
        )
        book2.authors.append(author2)
        db.add(book2)

        db.commit()
        print("✅ Data seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
