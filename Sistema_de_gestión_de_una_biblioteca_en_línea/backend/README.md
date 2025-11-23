# Running the Library Management System

## Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

## Setup Instructions

### 1. Create Environment File
Copy the example environment file and configure it with your credentials:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Then edit `.env` and update the values:
- `POSTGRES_PASSWORD`: Set a secure password
- `JWT_SECRET_KEY`: Generate a secure random key (e.g., using `openssl rand -hex 32`)

### 2. Start the Services
From the `backend` directory, run:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- FastAPI backend on port 8009

### 3. Apply Database Migrations
Once the containers are running, apply the migrations:

```bash
docker-compose exec backend alembic upgrade head
```

### 4. Seed the Database
Populate the database with initial data:

```bash
docker-compose exec backend python seed_data.py
```

### 5. Access the Application
- API Documentation: http://localhost:8009/docs
- Alternative API Docs: http://localhost:8009/redoc

## Default Login Credentials
After seeding, you can use these credentials:

- **Admin**: admin@library.com / admin123
- **User 1**: john@example.com / password123
- **User 2**: jane@example.com / password123

## Useful Commands

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f db
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes (Clean Database)
```bash
docker-compose down -v
```

### Restart Services
```bash
docker-compose restart
```

### Run Tests
```bash
docker-compose exec backend pytest
```

### Create a New Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "Description of changes"
```

## Troubleshooting

### Database Connection Issues
If you see connection errors, ensure the database is fully started:
```bash
docker-compose logs db
```

### Port Already in Use
If port 8009 or 5432 is already in use, modify the ports in `docker-compose.yml`:
```yaml
ports:
  - "8010:8009"  # Change 8010 to any available port
```

### Reset Everything
To start fresh:
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python seed_data.py
```
