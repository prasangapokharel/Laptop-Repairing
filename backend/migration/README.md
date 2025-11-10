# Database Migration and Seeding Guide

## Quick Start

### Run All (Migrations + Seed)
```bash
python migration/run_all.py
```

### Run Migrations Only
```bash
alembic upgrade head
```

### Run Seed Only
```bash
python migration/run_seed.py
```

### Verify Seed Data
```bash
python migration/verify_seed.py
```

## Migration Commands

### Create New Migration
```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Seed Data

The seed script populates:
- **5 Roles**: Admin, Technician, Reception, Accountant, Customer
- **4 Device Types**: Laptop, Desktop, Tablet, Smartphone
- **10 Brands**: Apple, Dell, HP, Lenovo, Asus, Acer, Samsung, Microsoft, Toshiba, Sony

## Production Setup

1. Set environment variables in `.env` file
2. Run migrations: `alembic upgrade head`
3. Run seed: `python migration/run_seed.py`
4. Verify: `python migration/verify_seed.py`

