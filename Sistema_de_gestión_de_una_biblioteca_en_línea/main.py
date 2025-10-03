from fastapi import FastAPI
import uvicorn
from infrastructure.web.controllers import book_controller, user_controller, library_controller
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi import Request, status

from domain.models.exceptions.resource import ResourceConflictError, ResourceNotFoundError


@asynccontextmanager
async def lifesfan(app: FastAPI):
    print(f"Iniciando la aplicación en el puerto 8008")
    yield
    print(f"Finalizando la aplicación en el puerto 8008")   


app = FastAPI(
    title="Servicio de Biblioteca",
    description="Una API para la gestión de préstamos y devoluciones de libros.",
    lifespan=lifesfan
)


app.include_router(book_controller.router)
app.include_router(library_controller.router)
app.include_router(user_controller.router)
 
    
@app.exception_handler(ResourceConflictError)
async def book_already_exists_exception_handler(request: Request, exc: ResourceConflictError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)}
    )
    
@app.exception_handler(ResourceNotFoundError)
async def book_not_found_exception_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )
    

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Error interno del servidor: {str(exc)}"}
    )   

# Datos de prueba  
# Crear libros
# book1 = Book(
#     id=str(uuid.uuid4()),
#     isbn=ISBN("978-0132350884"), 
#     title="Clean Code",
#     author="Robert C. Martin",
#     available_copies=5
# )
# book2 = Book(
#     id=str(uuid.uuid4()),
#     isbn=ISBN("978-0134494166"), 
#     title="Clean Architecture",
#     author="Robert C. Martin",
#     available_copies=1
# )
# book3 = Book(
#     id=str(uuid.uuid4()),
#     isbn=ISBN("978-1491910792"), 
#     title="Building Microservices",
#     author="Sam Newman",
#     available_copies=2
# )
    
# Si el script se ejecuta directamente, arranca el servidor
if __name__ == "__main__":
    uvicorn.run("main:app", port=8008, reload=True)