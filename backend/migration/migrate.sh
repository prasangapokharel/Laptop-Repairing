#!/bin/bash
# Create a new migration
alembic revision --autogenerate -m "$1"

