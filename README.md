# Me-API Playground

A personal API playground project that hosts my profile, projects, and skills.
Built with FastAPI, React (Vite), PostgreSQL, and Docker.

## Architecture

[ Frontend (React) ] -> [ Nginx ] -> (Port 3000)
       |
       v
(API Requests)
       |
       v
[ Backend (FastAPI) ] -> (Port 8000)
       |
       v
[ PostgreSQL DB ] -> (Port 5432)

## Prerequisites

- Docker & Docker Compose

## Local Setup & Production

1. **Clone the repository** (if not already local)
2. **Build and Run**:
   ```bash
   docker-compose up --build
   ```
3. **Access**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health Check: [http://localhost:8000/health](http://localhost:8000/health)

## API Examples

**Get Profile:**
```bash
curl http://localhost:8000/profile
```

**Search:**
```bash
curl "http://localhost:8000/search?q=python"
```

## Database

The database is automatically seeded with sample data on first run from `database/seed.sql`.
Schema is defined in `models.py` (via SQLAlchemy) and `database/schema.sql`.

## Known Limitations

- No authentication (public API).
- Minimal error handling.
- Styles are basic (Tailwind).
