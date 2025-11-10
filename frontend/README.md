# Frontend - Laptop Repair Store Management System

## Quick Start

### Option 1: Use the Start Script (Easiest)

Simply double-click `start.bat` in the frontend folder. This will:
- ✅ Check Python installation
- ✅ Create virtual environment (if needed)
- ✅ Install backend dependencies
- ✅ Run database migrations
- ✅ Seed the database
- ✅ Start backend server (http://localhost:8000)
- ✅ Start frontend server (http://localhost:3000)

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd ../backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
alembic upgrade head
```

6. Seed database:
```bash
python migration/run_seed.py
```

7. Start backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file (copy from `.env.example`):
```bash
cp .env.example .env.local
```

3. Start development server:
```bash
npm run dev
```

## Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# Application Configuration
NEXT_PUBLIC_APP_NAME=Laptop Repair Store Management
NEXT_PUBLIC_APP_VERSION=1.0.0

# Environment
NEXT_PUBLIC_ENV=development
```

## API Configuration

The frontend is configured to connect to:
- **Base URL**: `http://localhost:8000`
- **API Version**: `v1`
- **Full API URL**: `http://localhost:8000/v1`

All API calls automatically use the `/v1` prefix.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── src/
│   ├── app/          # Next.js app directory
│   ├── components/   # React components
│   ├── hooks/        # Custom React hooks
│   ├── lib/          # Utilities and API client
│   ├── types/        # TypeScript types
│   └── utils/        # Helper functions
├── .env.example      # Environment variables template
├── start.bat         # Quick start script (Windows)
└── package.json      # Dependencies
```

## Troubleshooting

### Backend not starting
- Check if Python is installed: `python --version`
- Check if port 8000 is available
- Check backend logs in the "Backend Server" window

### Frontend not connecting to backend
- Verify backend is running on http://localhost:8000
- Check `.env.local` file has correct `NEXT_PUBLIC_API_BASE_URL`
- Check browser console for CORS errors

### Migration errors
- Make sure MySQL is running
- Check database credentials in backend `.env` file
- Try running migrations manually: `cd ../backend && alembic upgrade head`

## Support

For issues or questions, check:
- Backend API documentation: http://localhost:8000/docs
- Postman collection: `LaptopRepair.json`

