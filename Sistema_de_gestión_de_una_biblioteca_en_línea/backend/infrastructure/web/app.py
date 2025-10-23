from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers.author_controller import router as author_router
from .controllers.book_controller import router as book_router
from .controllers.user_controller import router as user_router
from .controllers.library_controller import router as library_router
from .controllers.auth_controller import router as auth_router

app = FastAPI(title="Library API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(author_router, prefix="/authors", tags=["Autores"])
app.include_router(book_router, prefix="/books", tags=["Libros"])
app.include_router(user_router, prefix="/users", tags=["Usuarios"])
app.include_router(library_router, prefix="/library", tags=["Biblioteca"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de la Biblioteca"}