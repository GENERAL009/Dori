# Dori - Family Medicine Tracker

Oilaviy dorilarni boshqarish tizimi. Erkak va ayol uchun shifokor yozib bergan dorilar, ukollar va kapelnitsalarni kuzatib borish.

## Quick Start

```bash
docker compose up -d
```

Brauzerda ochish: http://localhost

**PIN kod:** `1234`

## Features

- PIN-based authentication (shaxsiy foydalanish)
- Erkak/Ayol profil tanlash
- Bugungi dorilar dashboard
- Dori va vitamin tracking
- Kapelnitsa (IV infusion) monitoring
- Kalendar ko'rinish
- Statistika va grafiklar
- Real-time notification (WebSocket)
- Retsept saqlash
- Mobile responsive dizayn

## Tech Stack

**Backend:** FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis, APScheduler
**Frontend:** React, TypeScript, Vite, TailwindCSS, shadcn/ui, React Query
**Infrastructure:** Docker, Nginx, Alembic

## Project Structure

```
Dori/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # REST API endpoints
│   │   ├── core/                # Config, security, exceptions
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access layer
│   │   ├── scheduler/           # APScheduler tasks
│   │   ├── notifications/       # WebSocket & browser notifications
│   │   ├── parsers/             # OCR prescription parser interface
│   │   └── database/            # Session & seed data
│   ├── alembic/                 # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                 # API client & endpoints
│   │   ├── components/          # UI components
│   │   ├── pages/               # Route pages
│   │   ├── hooks/               # Custom hooks
│   │   ├── stores/              # Zustand stores
│   │   ├── types/               # TypeScript types
│   │   └── lib/                 # Utilities
│   ├── Dockerfile
│   └── package.json
├── nginx/nginx.conf
├── docker-compose.yml
└── .env
```

## API Documentation

Swagger UI: http://localhost/api/docs
ReDoc: http://localhost/api/redoc

## Seed Data

Retseptdagi barcha dorilar avtomatik kiritilgan:

**Ayol (8 ta dori):** Сейодин, Vitamin E NERO, Vitamin D, Квинофолик, Андровумен, Достинекс, Сибисил, Дюфастон

**Erkak (4 ta dori + 3 ta kapelnitsa):** Цистокс Д форте, Фурамаг, Уростим, Олинорм, Орнидазол, Левомак, Фуцис

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
