# Kenyan CBE Assessment Management System

A multi-tenant school assessment platform for Kenya's Competency-Based Education workflows.

## Project status

See [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md) for the authoritative continuation brief, decisions, milestones, and next actions.

## Stack

- Backend: Python 3.12+, FastAPI, SQLAlchemy 2 async, Alembic, Pydantic v2
- Data/services: PostgreSQL, Redis, Arq
- Frontend: Next.js App Router, React, TypeScript, Tailwind CSS
- Payments: Paystack only (M-Pesa Express/STK Push, cards, subaccounts, transaction splits, subscriptions)

## Local development

Copy `.env.example` to `.env`, then run `docker compose up --build`. See `backend/README.md` and `frontend/README.md` as those milestones land.

## Scope guardrails

This is not a generic school ERP. Do not add transport, library, hostel, or HR/payroll modules. Do not use floating-point values for money. All school-owned records must be tenant-scoped. Paystack webhooks must be signature-verified against raw request bytes and processed idempotently.
