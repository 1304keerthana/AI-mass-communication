# AI-Powered Mass Communication Platform Backend

This scaffold provides a backend for an AI-powered multilingual communication platform.

## Features

- User registration, authentication, and role-based access control
- Audience member database with segmentation filters
- Campaign creation and template management
- AI content generation, translation, and sentiment analysis stubs
- Campaign status management and engagement tracking

## Getting Started

1. Create a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Start PostgreSQL with Docker Compose:

   ```bash
   docker compose up -d
   ```

4. Run the app using `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
5. Register users at `/auth/register` and obtain tokens at `/auth/token`.
6. Use the API endpoints to manage audience, templates, and campaigns.

## Architecture

- `app/main.py` - FastAPI endpoints and startup logic
- `app/models.py` - SQLModel data models and enums
- `app/schemas.py` - Pydantic request/response schemas
- `app/crud.py` - Database operations
- `app/auth.py` - JWT authentication and role guard
- `app/llm_service.py` - Stubbed AI content and translation service
- `app/database.py` - SQLite database initialization

## Notes

This scaffold uses stub implementations for AI and messaging features. Replace `AIService` methods with real LLM and translation integrations to enable production workflows.
