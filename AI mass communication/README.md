# AI-Based Multilingual Mass Communication & Public Awareness Management Platform

This repository contains the backend and frontend foundations for a clean architecture implementation of a mass communication and awareness management platform.

## Tech Stack

- Backend: FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, JWT Auth, python-jose, Passlib, Pydantic v2
- Frontend: React.js (Vite), TailwindCSS, React Router, React Query, Axios
- Database: PostgreSQL
- Version Control: Git

## Structure

- `backend/`
  - `app/` - FastAPI application
- `frontend/`
  - `src/` - React application

## Getting Started

1. Configure PostgreSQL and `.env` files.
2. Install backend dependencies with `pip install -r requirements.txt` or `pip install .`.
3. Install frontend dependencies with `npm install`.
4. Run backend: `npm run start` or `python -m uvicorn app.main:app --reload`.
5. Run frontend: `npm run dev`.
