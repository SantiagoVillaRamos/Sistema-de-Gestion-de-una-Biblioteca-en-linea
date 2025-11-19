# base ligera de Python
FROM python:3.10-slim
# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app
# Copiamos las dependencias e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copiamos todo el código fuente de la aplicación al contenedor
COPY . .
# Nota: La ejecución real se definirá en docker-compose.yml
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
