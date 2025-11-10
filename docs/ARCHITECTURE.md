# Project Architecture

## Overview

This is a production-grade, scalable, modular architecture for a Django backend and Next.js frontend application.

## Folder Structure

```
project-root/
├── backend/              # Django backend
│   ├── backend/          # Django project settings
│   │   ├── settings/     # Environment-based settings
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py       # Main URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/             # Django applications (modular)
│   │   ├── users/        # User management app
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── admin.py
│   │   │   └── index.py  # Module entry point
│   │   └── api/          # API layer
│   │       ├── views.py
│   │       ├── urls.py
│   │       ├── renderers.py  # ORJSON renderer
│   │       ├── parsers.py    # ORJSON parser
│   │       ├── pagination.py
│   │       ├── permissions.py
│   │       ├── filters.py
│   │       └── exceptions.py
│   ├── core/             # Shared utilities
│   │   ├── utils.py
│   │   └── validators.py
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── providers.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   └── user/
│   │   │       └── add/
│   │   │           └── page.tsx
│   │   ├── components/   # Reusable components
│   │   │   └── ui/
│   │   ├── lib/          # Libraries and configurations
│   │   │   └── api-client.ts
│   │   ├── types/        # TypeScript types
│   │   │   └── user.ts
│   │   ├── hooks/        # Custom React hooks
│   │   │   └── useUsers.ts
│   │   └── utils/        # Utility functions
│   │       ├── validation.ts
│   │       └── format.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.js
│
└── docs/                 # Documentation
    └── ARCHITECTURE.md
```

## Key Features

### Backend (Django)

1. **Modular App Structure**: Each feature is a separate Django app in `apps/`
2. **ORJSON Integration**: Fast JSON serialization using ORJSON
3. **PostgreSQL**: Production-ready database backend
4. **Environment-based Settings**: Separate configs for dev/prod
5. **API Layer**: Separate API app for clean separation
6. **Module Entry Points**: `index.py` files for easy imports

### Frontend (Next.js)

1. **App Router**: Modern Next.js 14 App Router structure
2. **TypeScript**: Full type safety
3. **React Query**: Efficient data fetching and caching
4. **Modular Components**: Reusable UI components
5. **Custom Hooks**: Business logic in hooks
6. **Type Safety**: Shared types between frontend/backend

## Development Workflow

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your database
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Adding New Features

### Backend (Django App)

1. Create new app: `python manage.py startapp <app_name> apps/<app_name>`
2. Add models in `apps/<app_name>/models.py`
3. Create serializers in `apps/<app_name>/serializers.py`
4. Add views in `apps/api/views.py` or create app-specific views
5. Register URLs in `apps/api/urls.py`
6. Create `apps/<app_name>/index.py` for module exports

### Frontend (Next.js Page)

1. Create page in `src/app/<feature>/page.tsx`
2. Add types in `src/types/<feature>.ts`
3. Create API hooks in `src/hooks/use<Feature>.ts`
4. Add reusable components in `src/components/`

## API Structure

All API endpoints are under `/api/v1/`:

- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}/` - Get user
- `GET /api/v1/users/me/` - Get current user

## Best Practices

1. **No Code Duplication**: Extract shared logic to `core/` or `utils/`
2. **Type Safety**: Use TypeScript types and Zod schemas
3. **Modular Design**: Each feature is self-contained
4. **Clean Code**: Follow SOLID principles, max 50 LOC per function
5. **Performance**: Use ORJSON for fast JSON serialization
6. **Scalability**: Design for horizontal scaling

## Team Collaboration

- **Frontend Developers**: Work in `frontend/` directory
- **Backend Developers**: Work in `backend/apps/` directory
- **API Developers**: Work in `backend/apps/api/` directory
- Each team can work independently without conflicts
