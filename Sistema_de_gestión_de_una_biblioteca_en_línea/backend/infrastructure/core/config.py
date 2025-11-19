import os
from dotenv import load_dotenv
from pathlib import Path    

env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
if env_path.exists():
    print(f"\n Cargando el archivo de configuración: {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    print(f"\n No se encontró el archivo de configuración: {env_path}. Asegúrate de que exista un archivo .env este en la raíz del proyecto.")   


class Config:
    """Clase de configuración para la aplicación."""

    # Configuración de la base de datos
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: str = int(os.getenv('POSTGRES_PORT'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    
    # Configuración del servidor
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}" 
    
settings = Config()