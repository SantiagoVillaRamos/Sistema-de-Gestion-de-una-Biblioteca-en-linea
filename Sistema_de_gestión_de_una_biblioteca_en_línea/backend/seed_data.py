"""
Seed script to populate the database with initial data.
Run this after applying migrations with: python seed_data.py
"""
from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.models import UserModel, BookModel, AuthorModel
import uuid
import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_data():
    """Seed the database with initial users, authors, and books."""
    
    db = SessionLocal()
    try:
        # Create admin user
        admin_user = UserModel(
            id=str(uuid.uuid4()),
            name="Admin User",
            email="admin@library.com",
            password_hash=hash_password("admin123"),
            user_type="premium",
            roles="ADMIN,MEMBER",
            is_active=True
        )
        db.add(admin_user)
        
        # Create regular users
        user1 = UserModel(
            id=str(uuid.uuid4()),
            name="John Doe",
            email="john@example.com",
            password_hash=hash_password("password123"),
            user_type="general",
            roles="MEMBER",
            is_active=True
        )
        db.add(user1)
        
        user2 = UserModel(
            id=str(uuid.uuid4()),
            name="Jane Smith",
            email="jane@example.com",
            password_hash=hash_password("password123"),
            user_type="premium",
            roles="MEMBER",
            is_active=True
        )
        db.add(user2)
        
        # Create authors
        author1_id = str(uuid.uuid4())
        author1 = AuthorModel(
            id=author1_id,
            name="George Orwell"
        )
        db.add(author1)
        
        author2_id = str(uuid.uuid4())
        author2 = AuthorModel(
            id=author2_id,
            name="J.K. Rowling"
        )
        db.add(author2)
        
        author3_id = str(uuid.uuid4())
        author3 = AuthorModel(
            id=author3_id,
            name="Isaac Asimov"
        )
        db.add(author3)
        
        # Create books
        book1 = BookModel(
            id=str(uuid.uuid4()),
            isbn="978-0-452-28423-4",
            title="1984",
            author_id=author1_id,
            description="A dystopian social science fiction novel and cautionary tale.",
            available_copies=5
        )
        db.add(book1)
        
        book2 = BookModel(
            id=str(uuid.uuid4()),
            isbn="978-0-7475-3269-9",
            title="Harry Potter and the Philosopher's Stone",
            author_id=author2_id,
            description="The first novel in the Harry Potter series.",
            available_copies=3
        )
        db.add(book2)
        
        book3 = BookModel(
            id=str(uuid.uuid4()),
            isbn="978-0-553-29337-0",
            title="Foundation",
            author_id=author3_id,
            description="The first novel in Isaac Asimov's Foundation Trilogy.",
            available_copies=4
        )
        db.add(book3)
        
        book4 = BookModel(
            id=str(uuid.uuid4()),
            isbn="978-0-452-28424-1",
            title="Animal Farm",
            author_id=author1_id,
            description="An allegorical novella about Soviet totalitarianism.",
            available_copies=6
        )
        db.add(book4)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   - Created 3 users (admin@library.com, john@example.com, jane@example.com)")
        print(f"   - Created 3 authors")
        print(f"   - Created 4 books")
        print("\n📝 Login credentials:")
        print("   Admin: admin@library.com / admin123")
        print("   User1: john@example.com / password123")
        print("   User2: jane@example.com / password123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
