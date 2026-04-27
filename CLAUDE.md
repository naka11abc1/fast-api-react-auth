# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

Full-stack web application with JWT authentication using httpOnly Cookies.

```
Browser → Nginx (port 80) → React SPA
                          → /api/* → FastAPI (port 8000) → PostgreSQL
```

- **Backend**: FastAPI + SQLAlchemy + Alembic (`backend/`)
- **Frontend**: React + TypeScript + Vite (`frontend/`)
- **Auth**: JWT stored in httpOnly Cookie, validated via FastAPI `Depends`

## Commands

### Local Development

```bash
# Start backend + DB
docker compose up -d --build

# Run backend tests
docker compose exec api pytest tests/

# Run a single test
docker compose exec api pytest tests/test_auth.py::test_login_success

# Run DB migrations
docker compose exec api alembic upgrade head

# Create a new migration after model changes
docker compose exec api alembic revision --autogenerate -m "description"

# Frontend dev server (runs outside Docker)
cd frontend && npm run dev

# Frontend lint
cd frontend && npm run lint
```

### Production Deploy

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec api alembic upgrade head
```

## Backend Structure

Authentication is centralized in `backend/app/deps.py` via `get_user_info` dependency. Routes requiring auth use `dependencies=[Depends(get_user_info)]` at the router level in `backend/main.py`.

- `app/routers/` — Endpoint definitions. `auth.router` is public, `user.router` requires auth.
- `app/services/` — Business logic and DB queries. DB access goes through services, not directly in routers.
- `app/schemas/` — Pydantic models for request/response validation.
- `app/models/` — SQLAlchemy ORM models.
- `app/deps.py` — `get_db` (DB session) and `get_user_info` (auth guard).

Password hashing uses `bcrypt` directly (not passlib).

## Frontend Structure

- `src/features/` — Feature-based modules (auth, user). Each has `api.ts`, `types.ts`, and components.
- `src/pages/` — Page components (`LoginPage`, `DashboardPage`).
- `src/hooks/useAuth.ts` — Calls `GET /auth/user` to check auth state on mount.
- `src/components/PrivateRoute.tsx` — Redirects to `/login` if unauthenticated.
- `src/lib/axios.ts` — Axios instance with `withCredentials: true` for Cookie support.

`VITE_API_URL` controls the API base URL. Local: `.env.local`, Production: `.env.production` (set to `/api`).

## Environment Variables

Backend `.env`:
```
DATABASE_URL=postgresql://postgres:password@db:5432/appdb
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173
```

## Testing

Tests use SQLite in-memory DB. The `db` fixture in `tests/conftest.py` provides a shared session used by both `client` (via `override_get_db`) and `test_user` fixture.

GitHub Actions runs tests before deploy with `DATABASE_URL=sqlite:///./test.db`.