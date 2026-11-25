# Kenyan CBE Assessment Management System

An independent, focused MVP for Kenyan Competency-Based Education assessment workflows.

## Start here
- **Project continuation state:** [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md)
- **Architecture decisions:** [docs/decisions/](docs/decisions/)
- Backend: [backend/README.md](backend/README.md)
- Frontend: [frontend/README.md](frontend/README.md)

## Stack
- Backend: Python 3.12+, FastAPI, SQLAlchemy 2 async, Alembic, Pydantic v2
- Data/jobs: PostgreSQL, Redis, Arq
- Frontend: Next.js App Router, React, TypeScript, Tailwind CSS
- Payments: Paystack only

## Local development
Copy `.env.example` to `.env`, replace development secrets, then run `docker compose up --build`.

## Strict scope
No transport, library, hostel, HR/payroll or generic ERP modules. Money is stored as BIGINT KES cents. Every school-owned record must be tenant scoped. Paystack webhooks must be verified against raw request bytes and processed idempotently.

Demo curriculum content is illustrative and must not be represented as official KICD content.
