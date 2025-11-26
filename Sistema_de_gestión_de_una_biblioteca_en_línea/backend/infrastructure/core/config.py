import os
from dotenv import load_dotenv
from pathlib import Path    

# Try to load .env from multiple possible locations
# 1. Current working directory (Docker: /app/.env)
# 2. Backend directory (local development)
env_paths = [
    Path.cwd() / '.env',
    Path(__file__).resolve().parent.parent.parent / '.env',
]

for env_path in env_paths:
    if env_path.exists():
        print(f"\n✅ Cargando configuración desde: {env_path}")
        load_dotenv(dotenv_path=env_path)
        break
else:
    print(f"\n⚠️  No se encontró archivo .env, usando variables de entorno del sistema")


class Config:
    """Clase de configuración para la aplicación."""

    # Detect environment
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')

    # Configuración de la base de datos
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'library_db')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    
    # 🔒 SECURITY: Database password - no default in production
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    if not POSTGRES_PASSWORD:
        if ENVIRONMENT == 'production':
            raise ValueError("🔒 SECURITY ERROR: POSTGRES_PASSWORD must be set in production environment")
        else:
            # Development fallback with warning
            POSTGRES_PASSWORD = 'postgres'
            print("⚠️  WARNING: Using default POSTGRES_PASSWORD='postgres' (development only)")
    
    # 🔒 SECURITY: JWT secret - no default in production
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    if not SECRET_KEY:
        if ENVIRONMENT == 'production':
            raise ValueError(
                "🔒 SECURITY ERROR: JWT_SECRET_KEY must be set in production environment.\n"
                "Generate a secure key with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
            )
        else:
            # Development fallback with warning
            SECRET_KEY = 'dev_secret_key_INSECURE_DO_NOT_USE_IN_PRODUCTION'
            print("⚠️  WARNING: Using insecure default JWT_SECRET_KEY (development only)")
            print("   Generate a secure key with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
    
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración del servidor - Usar postgresql+psycopg2 para psycopg2-binary
    DATABASE_URL: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}" 
    
settings = Config()